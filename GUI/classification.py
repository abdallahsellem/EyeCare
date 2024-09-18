from tensorflow.keras.models import load_model
import keras
import tensorflow as tf
from PIL import Image, ImageDraw
import numpy as np
import cv2 as cv
from threading import Thread
import datetime


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


def create_rounded_image(im, radius):
    # Create the mask with rounded corners
    mask = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + im.size, radius, fill=255)

    # Create a new image with a white background to use the mask
    rounded_im = Image.new('RGB', im.size, (255, 255, 255))
    rounded_im.paste(im, mask=mask)

    return rounded_im


def loadImg(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_array = np.array(img)
    return img_array


def resizeImg(image, target_width=512, target_height=512):
    original_height, original_width = image.shape[:2]
    aspect_ratio = original_width / original_height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_width = int(target_height * aspect_ratio)
        new_height = target_height

    resized_image = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_CUBIC)
    canvas = 255 * np.ones((target_height, target_width, 3), dtype=np.uint8)

    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image

    return canvas


def crop(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Detect circles using Hough Circle Transform
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, dp=1, minDist=20,
                              param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circle to integers
        circles = np.round(circles[0, :]).astype("int")

        # Assuming there's only one circle, extract its coordinates and radius
        (x, y, r) = circles[0]

        # Create a mask for the circle
        mask = np.zeros_like(gray)
        cv.circle(mask, (x, y), r, 255, thickness=-1)

        # Crop the circle from the original image using the mask
        masked_image = cv.bitwise_and(image, image, mask=mask)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(max_contour)
        cropped_image = masked_image[y:y + h, x:x + w]
        resized_image = cv.resize(cropped_image, (224, 224))
        return resized_image, True
    else:
        print("No circles detected.")
        return image, False


def enhanceImg(img):
    conv_img = cv.cvtColor(img, cv.COLOR_RGB2YCrCb)
    Y_channel = conv_img[:, :, 0]
    Y_channel = Y_channel.astype(np.uint8)

    clahe = cv.createCLAHE(clipLimit=10.0, tileGridSize=(16, 16))
    cl = clahe.apply(Y_channel)

    merged = cv.merge((cl, conv_img[:, :, 1], conv_img[:, :, 2]))
    modified_img = cv.cvtColor(merged, cv.COLOR_YCrCb2RGB)

    return modified_img




