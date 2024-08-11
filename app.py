import streamlit as st
import os
import base64
from utils import process_image
from PIL import Image
import io

def add_border(image_path, border_size=5, border_color=(0, 0, 0)):
    image = Image.open(image_path)
    new_size = (image.size[0] + 2*border_size, image.size[1] + 2*border_size)
    new_image = Image.new("RGB", new_size, border_color)
    new_image.paste(image, (border_size, border_size))
    return new_image


def main():
    st.set_page_config(page_title="Adobe Gensolve Curvetopia Assessment", layout="wide")
    st.title("Adobe Gensolve Curvetopia Assessment")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Create a temporary directory to store output files
        output_dir = "temp_output"
        os.makedirs(output_dir, exist_ok=True)
        output_path_base = os.path.join(output_dir, "output")

        # Process the uploaded file
        original_plot_path, smoothed_output_path, original_symmetry, smoothed_symmetry = process_image(uploaded_file, output_path_base)

        # Display input and output plots side by side
        col1, col2 = st.columns(2)
        
        # Input plot (original)
        if os.path.exists(original_plot_path):
            with col1:
                st.subheader("Input")
                original_image = add_border(original_plot_path)
                st.image(original_image, use_column_width=True)


        # Output plot (smoothed)
        if os.path.exists(smoothed_output_path):
            with col2:
                st.subheader("Output")
                smoothed_image = add_border(smoothed_output_path)
                st.image(smoothed_image, use_column_width=True)
    

        # Provide download links for output files
        st.subheader("Download Results")
        for ext in [".svg", ".png", ".csv"]:
            file_path = output_path_base + ext
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    contents = file.read()
                    b64 = base64.b64encode(contents).decode()
                    href = f'<a href="data:file/{ext[1:]};base64,{b64}" download="output{ext}">Download {ext[1:].upper()} file</a>'
                    st.markdown(href, unsafe_allow_html=True)

        # Clean up temporary files
        for ext in [".svg", ".png", ".csv"]:
            os.remove(output_path_base + ext)
        os.remove(original_plot_path)
        os.rmdir(output_dir)

if __name__ == "__main__":
    main()