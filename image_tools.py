import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Converts png image to grayscale and keeps alpha channel
def png_grayscale(image):
    bgr = image[:,:,:3]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    alpha = image[:,:,3]
    return np.dstack([bgr, alpha])

# Loads image to numpy array from path
def load_image(path):
    ext = os.path.splitext(path)[1]
    if ext == ".jpg":
        image = cv2.imread(path, 0)
    elif ext == ".png":
        image = png_grayscale(cv2.imread(path, cv2.IMREAD_UNCHANGED))
    return np.asarray(image).copy()

# Shows image with pyplot
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.show()

# Resizes image keeping its original aspect ratio
def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    shape = (width, height)
    resized = cv2.resize(image, shape, interpolation=cv2.INTER_AREA)
    return np.asarray(resized).copy()

# Blur images with openCV Gaussian blur
def blur_image(image):
    kernel_size = (81,81)
    return cv2.GaussianBlur(image, kernel_size, 0)