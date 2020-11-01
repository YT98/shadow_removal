from numpy import asarray
import cv2
import matplotlib.pyplot as plt

# Loads image to numpy array from path
def load_image(path):
    image = cv2.imread(path, 0)
    return asarray(image).copy()

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
    return asarray(resized).copy()

# Blur images with openCV Gaussian blur
def blur_image(image):
    kernel_size = (81,81)
    return cv2.GaussianBlur(image, kernel_size, 0)