import numpy as np
import cv2 as cv
from PIL import Image

target_size = (512, 512)


################

def find_contours(binary_mask):
    _, binary_mask = cv.threshold(binary_mask, 1, 255, cv.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    closed_mask = cv.morphologyEx(binary_mask, cv.MORPH_CLOSE, kernel)
    opened_mask = cv.morphologyEx(closed_mask, cv.MORPH_OPEN, kernel)
    dilated_mask = cv.dilate(opened_mask, kernel, iterations=1)
    final_mask = cv.erode(dilated_mask, kernel, iterations=1)
    contours, _ = cv.findContours(final_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours


def crop_contours(image, contours):
    max_contour = max(contours, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(max_contour)
    cropped_image = image[y:y + h, x:x + w]
    return cropped_image


def apply_clahe(image):
    """Applies CLAHE to an image for contrast enhancement using OpenCV."""
    if not isinstance(image, np.ndarray):
        image = np.array(image)
    # Convert image to grayscale
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Create CLAHE object
    clahe = cv.createCLAHE(clipLimit=2.5)

    # Apply CLAHE
    enhanced_image = clahe.apply(gray_image)

    # Convert back to RGB if needed
    enhanced_image = cv.cvtColor(enhanced_image, cv.COLOR_GRAY2BGR)
    return enhanced_image


def brightness_enhancment(image):
    brightness_image = cv.convertScaleAbs(image, alpha=1.3, beta=20)
    #     image_rgb=cv.cvtColor(brightness_image, cv.COLOR_BGR2RGB)
    image_bgr = brightness_image
    return image_bgr


def gamma_correction(image):
    # Gamma Correction
    gamma = 1.2
    lookup_table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected_image = cv.LUT(image, lookup_table)
    #     image_rgb=cv.cvtColor(gamma_corrected_image, cv.COLOR_BGR2RGB)
    image_bgr = gamma_corrected_image
    return image_bgr


################

def read_image_with_preprocess(img_path, target_size=target_size):
    # Read image
    image = Image.open(img_path)
    image = image.convert("RGB")

    # Resize image
    image = image.resize(target_size)
    image = apply_clahe(image)
    image = brightness_enhancment(image)
    image = gamma_correction(image)
    image_array = np.array(image)

    return image_array

def read_image(img_path, target_size=target_size):
    # Read image
    image = Image.open(img_path)
    image = image.convert("RGB")

    # Resize image
    image = image.resize(target_size)
    image_array = np.array(image)

    return image_array