from image_tools import load_image, show_image, resize_image, blur_image
from file_tools import get_silhouettes
import cv2
import random

class Mask:
    def __init__(self):
        self.silhouettes = []
        for file in get_silhouettes():
            self.silhouettes.append(load_image(file))

    # Randomizes shadow size
    def random_size_silhouettes(self):
        new_silhouettes = []
        for sil in self.silhouettes:
            # Randomize size increase
            increase = random.randint(150, 350)
            new_silhouettes.append(
                resize_image(sil, increase)
            )
        self.silhouettes = new_silhouettes

    # Blur silouettes
    def blur_silhouettes(self):
        new_silhouettes = []
        for sil in self.silhouettes:
            new_silhouettes.append(blur_image(sil))
        self.silhouettes = new_silhouettes

    # Applies shadow on given image
    def mask_image(self, shadow, image):
        new_image = image.copy()
        alpha = 0.6
        row, cols = shadow.shape
        roi = new_image[new_image.shape[0]-row:, new_image.shape[1]-cols:]
        shadowed_roi = cv2.addWeighted(roi, 1-alpha, shadow, alpha,0)
        new_image[new_image.shape[0]-row:, new_image.shape[1]-cols:] = shadowed_roi
        return new_image

    # Applies all shadows on given image
    def mask_all_silhouettes(self, image):
        shadowed_images = []
        for sil in self.silhouettes:
            new_image = self.mask_image(sil, image)
            shadowed_images.append(new_image)
        return shadowed_images