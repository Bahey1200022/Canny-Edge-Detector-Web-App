# Canny Edge Detection Web Application

This project is a web application built with Flask that performs Canny edge detection on uploaded images. Users can upload an image and specify parameters for the detection algorithm, and the processed image will be returned.

## Project Structure

- `app.py`: Main application file containing the Flask server and route definitions.
- `cannyFunction.py`: Contains custom functions for Canny edge detection.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory containing static files like CSS and JavaScript.

## Installation

1. Clone the repository

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Ensure you are in the project directory and the virtual environment is activated.
2. Run the Flask application:
    ```bash
    python app.py
    ```

3. Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

### Routes

- `/`: Renders the main HTML page where users can upload images and set parameters.
- `/upload`: Handles image uploads and returns the processed image.

### Parameters

For Canny edge detection:
- `sigma`: Standard deviation for Gaussian blur.
- `high`: High threshold ratio for Canny edge detection.
- `low`: Low threshold ratio for Canny edge detection.
- `kernel`: Kernel size for Gaussian blur.
- `image_data`: Base64 encoded image data.

## Functions

### `cannyFunction.py`

#### `convert_rgb_to_bgr(image)`
Converts an RGB image to BGR format.

#### `gaussian_kernel(image, kernel_size, sigma=None)`
Applies Gaussian blur to the input image.

#### `sobel_filters(image)`
Applies Sobel filters to the input image for edge detection.

#### `non_max_suppression(magnitude_image, gradient_angle)`
Performs non-maximum suppression on the gradient magnitude image.

#### `threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09)`
Applies double thresholding to the edge magnitude image.

#### `hysteresis(edge_image)`
Performs hysteresis thresholding on the edge magnitude image.

## Dependencies

- Flask
- OpenCV
- NumPy
- PIL (Pillow)
- SciPy

## Authors

| Name | GitHub | LinkedIn |
| ---- | ------ | -------- |
| Omar Adel Hassan | [@Omar_Adel](https://github.com/omar-adel1) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/omar-adel-59b707231/) |
| Sharif Ehab | [@Sharif_Ehab](https://github.com/SharifEhab) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sharif-elmasry-b167a3252/) |
| Mostafa Khaled | [@Mostafa_Khaled](https://github.com/MostafaDarwish93) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mostafa-darwish-75a29225b/) |
| Bahey Ismail | [@Bahey_Ismail ](https://github.com/Bahey1200022) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bahey-ismail-1602431a4/) |
