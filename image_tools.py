import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

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
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    elif ext == ".png":
        image = png_grayscale(cv2.imread(path, cv2.IMREAD_UNCHANGED))
    return np.asarray(image).copy()

# Shows image with pyplot
def show_image(image):
    plt.imshow(image, cmap="gray")
    plt.show()

# Blur images with openCV Gaussian blur
def blur_image(image):
    kernel_size = (81,81)
    return cv2.GaussianBlur(image, kernel_size, 0)
    