# Curvetopia: Advanced Shape Analysis and Regularization

This repository contains our solution for the Adobe gensolve hackathon challenge "CURVETOPIA: A Journey into the World of Curves". Our project focuses on identifying, regularizing, and beautifying 2D curves using advanced computer vision techniques.

## Project Overview

We have developed a comprehensive solution that addresses the three main tasks outlined in the challenge:

1. Curve Regularization
2. Symmetry Analysis
3. Curve Completion

Our approach utilizes advanced computer vision libraries such as OpenCV and Cairo to achieve robust shape detection and regularization.

## Key Features

- Identification and regularization of basic shapes (straight lines, circles, ellipses, rectangles, polygons, stars)
- Detection of reflection symmetries in closed shapes
- Curve completion for occluded shapes, including both connected and disconnected occlusions

## Implementation Details

We've implemented the following key components:

1. _Shape Regularization_: Algorithms to identify and regularize various geometric primitives.
2. _Symmetry Detection_: Methods to detect reflection symmetries in closed curves.
3. _Curve Completion_: Techniques to complete partially occluded curves naturally.

Our solution handles both isolated shapes and fragmented polylines as input, as specified in the problem statement.

## Demonstration Video

https://github.com/user-attachments/assets/760674c5-56d8-4ac7-a348-7d2cd2eaf0db

## Challenges Faced

We encountered several challenges during the development process, particularly in:

- Handling complex cases of curve completion
- Dealing with various occlusion scenarios

Despite these challenges, we've achieved good results with the provided test cases.

## Future Scope

Given the time constraints of the hackathon, we've focused on delivering a functional solution for the current test cases. For future development, we aim to:

1. Implement a Stable Diffusion Model to enhance our curve completion capabilities.
2. Train on an extensive dataset to improve performance on complex occlusion cases.
3. Refine our algorithms for even better accuracy and robustness.

With additional time and resources, we are confident in our ability to achieve even more impressive results, particularly in handling challenging occlusion scenarios.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```sh
    python3 -m pip install -r requirements.txt
```

### Installation

A step-by-step series of examples that tell you how to get a development env running:

1. Clone the repo:

   ```sh
   git clone https://github.com/An525ish/Adobe_Gensolve_Curvetopia.git
   ```

2. Install required packages:

   ```sh
   cd Adobe_Gensolve_Curvetopia
   ```

   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   streamlit run app.py
   ```

Visit `http://localhost:8501` in your web browser to view the application.

## Team Members

- [Anish Singh](https://github.com/An525ish) - Team Lead
- [Arya Sharma](https://github.com/aryasharma001) - Algorithm Developer

## Acknowledgments

We would like to thank Adobe for organizing this hackathon and providing us with this exciting challenge to tackle.
