import numpy as np
import scipy.stats as st
import cv2
import scipy.ndimage as ndimage

# Function to convert an RGB image to BGR format
def convert_rgb_to_bgr(image):
    """
    Convert an RGB image to BGR format using OpenCV's cv2.cvtColor() function.
    
    Parameters:
    - image: NumPy array representing the input RGB image.
    
    Returns:
    - bgr_image: NumPy array representing the image converted to BGR format.
    """
    bgr_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return bgr_image



def gaussian_kernel(image, kernel_size, sigma=None):
    """
    Applies Gaussian blur to the input image.

    Parameters:
    - image (numpy.ndarray): Input image.
    - kernel_size (int): Size of the Gaussian kernel.
    - sigma (float): Standard deviation of the Gaussian distribution.

    Returns:
    - numpy.ndarray: Blurred image.

    This function computes a Gaussian kernel using the given kernel size and sigma,
    applies the kernel to the input image using convolution, and returns the blurred image.

    Args:
    - x (int): The x-coordinate.
    - y (int): The y-coordinate.

    Formula:
    The Gaussian kernel is computed using the formula:
    G(x, y) = (1 / (2 * pi * sigma^2)) * e^((-1 * ((x - (kernel_size - 1) / 2)^2 + (y - (kernel_size - 1) / 2)^2)) / (2 * sigma^2))

    Normalization:
    The kernel is then normalized by dividing it by the sum of all kernel elements.

    Convolution:
    The blurred image is obtained by convolving the input image with the Gaussian kernel.
    """

    # Compute Gaussian kernel
    kernel = np.fromfunction(lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.e ** ((-1 * ((x - (kernel_size - 1) / 2) ** 2 + (y - (kernel_size - 1) / 2) ** 2)) / (2 * sigma ** 2)), (kernel_size, kernel_size))
    kernel /= np.sum(kernel)  # Normalize kernel

    # Convolve image with the kernel
    blur_img = ndimage.convolve(image, kernel, mode='constant')
    return blur_img



def sobel_filters(image):
    """
    Applies Sobel filters to an input image for edge detection.

    Args:
    - image (ndarray): Input image.

    Returns:
    - G (ndarray): Magnitude of the gradient.
    - theta (ndarray): Direction of the gradient.

    """

    # Define the Sobel kernels
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)

    # Convolve the image with the Sobel kernels
    gradient_x = cv2.filter2D(image, -1, kernel_x)
    gradient_y = cv2.filter2D(image, -1, kernel_y)

    # Compute the magnitude of the gradient
    magnitude = np.hypot(gradient_x, gradient_y)
    magnitude = magnitude / magnitude.max() * 255  # Normalize the magnitude

    # Compute the direction of the gradient
    direction = np.arctan2(gradient_y, gradient_x)

    return magnitude, direction

def non_max_suppression(magnitude_image, gradient_angle):
    height, width = magnitude_image.shape
    suppressed_image = np.zeros((height, width), dtype=np.int32) # resultant image

    # Convert radians to degrees and map negative angles to positive
    angle_degrees  = gradient_angle * 180. / np.pi
    angle_degrees [angle_degrees  < 0] += 180

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            neighbor_q  = 255  # Neighbor q
            neighbor_r  = 255  # Neighbor r

            # Based on the angle, select neighbors q and r for comparison
            if (0 <= angle_degrees[i, j] < 22.5) or (157.5 <= angle_degrees[i, j] <= 180):
                neighbor_r = magnitude_image[i, j - 1]
                neighbor_q = magnitude_image[i, j + 1]

            elif (22.5 <= angle_degrees[i, j] < 67.5):
                neighbor_r = magnitude_image[i - 1, j + 1]
                neighbor_q = magnitude_image[i + 1, j - 1]

            elif (67.5 <= angle_degrees[i, j] < 112.5):
                neighbor_r = magnitude_image[i - 1, j]
                neighbor_q = magnitude_image[i + 1, j]

            elif (112.5 <= angle_degrees[i, j] < 157.5):
                neighbor_r = magnitude_image[i + 1, j + 1]
                neighbor_q = magnitude_image[i - 1, j - 1]

            # If current pixel's magnitude is greater than or equal to both neighbors, keep it
            if (magnitude_image[i, j] >= neighbor_q) and (magnitude_image[i, j] >= neighbor_r):
                suppressed_image[i, j] = magnitude_image[i, j]
            else:
                suppressed_image[i, j] = 0

    return suppressed_image

def threshold(img, lowThresholdRatio = 0.05, highThresholdRatio = 0.09):
    """
    Applies double thresholding to an edge magnitude image.

    Args:
    - img (ndarray): Input image.
    - lowThreshold (float): Low threshold value.
    - highThreshold (float): High threshold value.

    Returns:
    - res (ndarray): Image after double thresholding.

    """

    # Print low and high thresholds
   # print(lowThreshold, highThreshold)

    highThreshold = np.max(img) * highThresholdRatio
    lowThreshold = highThreshold * lowThresholdRatio

    # Get image dimensions
    rows, cols  = img.shape

    # Initialize result array
    result  = np.zeros((rows, cols ), dtype=np.int32)

    # Define weak and strong values
    weak = np.int32(75)
    strong = np.int32(255)

    # Get indices of strong and weak pixels
    strong_i, strong_j = np.where(img >= highThreshold)
    zeros_i, zeros_j = np.where(img < lowThreshold)
    weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))

    # Assign values to result array based on thresholds
    result [strong_i, strong_j] = strong
    result [weak_i, weak_j] = weak

    return result 

    
def hysteresis(edge_image):
    """
    Performs hysteresis thresholding on an edge magnitude image.

    Args:
    - edge_image (ndarray): Input image.

    Returns:
    - thresholded_image (ndarray): Image after hysteresis thresholding.
    """

    # Get the dimensions of the image
    height, width  = edge_image.shape

    # Define weak and strong thresholds
    weak_threshold  = 75
    strong_threshold  = 255

    # Iterate over each pixel in the image
    for i in range(1, height - 1):
        for j in range(1, width  - 1):
            # Check if the current pixel intensity is weak
            if edge_image[i, j] == weak_threshold :
                try:
                    # Check if any neighboring pixel is strong
                    if ((edge_image[i + 1, j - 1] == strong_threshold ) or (edge_image[i + 1, j] == strong_threshold ) or (edge_image[i + 1, j + 1] == strong_threshold )
                            or (edge_image[i, j - 1] == strong_threshold ) or (edge_image[i, j + 1] == strong_threshold )
                            or (edge_image[i - 1, j - 1] == strong_threshold ) or (edge_image[i - 1, j] == strong_threshold ) or (edge_image[i - 1, j + 1] == strong_threshold )):
                        edge_image[i, j] = strong_threshold 
                    else:
                        edge_image[i, j] = 0
                except IndexError as e:
                    pass

    return edge_image

