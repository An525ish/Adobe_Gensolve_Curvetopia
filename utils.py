import cv2
import numpy as np
import os
import csv
import glob
import svgwrite
import cairosvg
import matplotlib.pyplot as plt

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def plot(path_XYs, title="", dpi=300):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8), dpi=dpi)
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, XYs in enumerate(path_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            if XY.shape[1] == 2:  # Ensure XY has two columns
                ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    ax.set_title(title)
    return fig
    
def detect_and_smooth_shapes(path_XYs):
    smoothed_paths = []
    for XYs in path_XYs:
        smoothed_XYs = []
        for XY in XYs:
            points = np.array(XY, dtype=np.int32)

            epsilon = 0.01 * cv2.arcLength(points, True)
            approx = cv2.approxPolyDP(points, epsilon, True)

            if len(approx) == 1:
                smoothed_XYs.append(XY)
            elif len(approx) == 2:
                smoothed_XYs.append(XY)
            elif len(approx) > 2:
                if len(approx) > 10:
                    ellipse = cv2.fitEllipse(points)
                    center, axes, angle = ellipse
                    major_axis, minor_axis = axes
                    if abs(major_axis - minor_axis) < 10:
                        smooth_points = cv2.ellipse2Poly(
                            (int(center[0]), int(center[1])),
                            (int(major_axis/2), int(minor_axis/2)),
                            int(angle), 0, 360, 5
                        )
                    else:
                        smooth_points = cv2.ellipse2Poly(
                            (int(center[0]), int(center[1])),
                            (int(major_axis/2), int(minor_axis/2)),
                            int(angle), 0, 360, 5
                        )
                else:
                    smooth_points = points
                smoothed_XYs.append(smooth_points)

        smoothed_paths.append(smoothed_XYs)
    return smoothed_paths

def draw_smooth_shapes(path_XYs, output_path_base):
    output_path_png = output_path_base + ".png"
    output_path_svg = output_path_base + ".svg"
    output_path_csv = output_path_base + ".csv"

    height, width = 1000, 1000
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    with open(output_path_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for XYs in path_XYs:
            for XY in XYs:
                points = np.array(XY, dtype=np.int32)
                cv2.polylines(canvas, [points], True, (0, 0, 0), 2, cv2.LINE_AA)
                for point in XY:
                    csvwriter.writerow(point)

    cv2.imwrite(output_path_png, canvas)
    polylines2svg(path_XYs, output_path_svg)

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    colours = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    for i, path in enumerate(paths_XYs):
        path_data = []
        c = colours[i % len(colours)]
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
            if not np.allclose(XY[0], XY[-1]):
                path_data.append(("Z", None))
        group.add(dwg.path(d=path_data, fill='none', stroke=c, stroke_width=2))
    dwg.add(group)
    dwg.save()
    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path,
                     parent_width=W, parent_height=H,
                     output_width=fact * W, output_height=fact * H,
                     background_color='white')
    
def analyze_symmetry(path_XYs):
    def detect_symmetry(XY):
        if XY.shape[0] < 5:
            return {'horizontal': False, 'vertical': False}
        
        hull = cv2.convexHull(XY.astype(np.float32))
        moments = cv2.moments(hull)
        if moments['m00'] == 0:
            return {'horizontal': False, 'vertical': False}
        
        centroid = (moments['m10'] / moments['m00'], moments['m01'] / moments['m00'])
        
        horizontal_score = symmetry_score(XY, centroid, 0)  # 0 degrees for horizontal
        vertical_score = symmetry_score(XY, centroid, 90)   # 90 degrees for vertical
        
        threshold = 0.05 * np.ptp(XY)
        return {
            'horizontal': horizontal_score < threshold,
            'vertical': vertical_score < threshold
        }

    def symmetry_score(XY, centroid, angle):
        rad = np.radians(angle)
        axis = np.array([np.cos(rad), np.sin(rad)])
        projected = np.dot(XY - centroid, axis)
        flipped = np.max(projected) - projected
        return np.mean(np.abs(projected - flipped))

    # Combine all points from all paths into a single array
    all_points = np.vstack([XY for XYs in path_XYs for XY in XYs])
    
    # Analyze symmetry for the entire figure
    symmetry = detect_symmetry(all_points)
    
    return symmetry

def process_image(csv_file, output_path_base):
    path_XYs = read_csv(csv_file)
    
    # Generate and save original plot
    original_plot = plot(path_XYs, "Original Plot")
    original_plot_path = output_path_base + "_original.png"
    original_plot.savefig(original_plot_path, dpi=300, bbox_inches='tight')
    plt.close(original_plot)

    # Analyze symmetry for original plot
    original_symmetry = analyze_symmetry(path_XYs)

    smoothed_paths = detect_and_smooth_shapes(path_XYs)
    draw_smooth_shapes(smoothed_paths, output_path_base)

    # The smoothed output is already saved by draw_smooth_shapes function
    smoothed_output_path = output_path_base + ".png"

    # Analyze symmetry for smoothed plot
    smoothed_symmetry = analyze_symmetry(smoothed_paths)

    return original_plot_path, smoothed_output_path, original_symmetry, smoothed_symmetry

def process_all_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    for csv_file in csv_files:
        base_name = os.path.basename(csv_file).split('.')[0]
        output_path_base = os.path.join(output_folder, base_name)
        process_image(csv_file, output_path_base)
