import cv2
import random
from image_tools import *
from file_tools import *
from perlin_noise import *


class Mask:
    def __init__(self, shadow):
        self.shadow = shadow
    
    # Resizes shadow keeping its original aspect ratio
    def scale(self, scale):
        width = int(self.shadow.shape[1] * scale / 100)
        height = int(self.shadow.shape[0] * scale / 100)
        shape = (width, height)
        scaled = cv2.resize(self.shadow, shape, interpolation=cv2.INTER_AREA)
        self.shadow = np.asarray(scaled)

    # Pads shadow with transparent pixels 
    # Returned image is of same shape as input image
    # Original shadow is always placed at the bottom but horizontal position is randomly determined
    def pad(self, image_shape):
        # TODO: Catch error if shadow is larger than img
        (img_h, img_w, _) = image_shape
        (shadow_h, shadow_w, _) = self.shadow.shape
        padding_top = img_h - shadow_h
        padding_left = random.randint(0, img_w - shadow_w)
        padding_right = img_w - shadow_w - padding_left
        padded = cv2.copyMakeBorder(
            self.shadow.copy(), 
            padding_top, 
            0, 
            padding_left, 
            padding_right, 
            cv2.BORDER_CONSTANT, 
            value=[255,255,255,0]
        )
        self.shadow = padded

    # Changes mask transparency
    def change_transparency(self, transparency):
        new_shadow = self.shadow.copy()
        new_a = new_shadow[:,:,3]
        new_a = np.array(new_a * transparency, dtype=np.uint8)
        r, g, b, old_a = cv2.split(new_shadow)
        new_shadow = cv2.merge((r,g,b,new_a))
        self.shadow = new_shadow

    # Applies mask to given image
    def apply(self, image):
        self.pad(image.shape)
        new_image = image.copy()
        # Normalize alpha channel from 0-255 to 0-1
        alpha = self.shadow[:,:,3] / 255.0
        # TODO try doing :3 instead of range(3)
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * self.shadow[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image

    # Applies gaussian blur to have a more realistic shadow
    def blur(self):
        # Pad shadow a little
        self.pad((self.shadow.shape[0]+50, self.shadow.shape[1]+50, 0))
        # Gaussian blur
        kernel_size = (15, 15)
        blurred = cv2.GaussianBlur(self.shadow, kernel_size, 15)
        self.shadow = blurred
        
    # Adds gaussian noise to have a more realistic shadow
    def add_noise(self):
        # Pad shadow a little
        self.pad((self.shadow.shape[0]+50, self.shadow.shape[1]+50, 0))
        # Create perlin mask
        scale = 100.0
        octaves = 4
        lacunarity = 3.0
        base = 1
        persistence = random.uniform(0.05, 0.25)
        mask = perlin_mask(
            (self.shadow.shape[0], self.shadow.shape[1]), 
            scale, 
            octaves, 
            persistence, 
            lacunarity, 
            base
        )
        # Add alpha channel to perlin mask
        new_mask = mask.copy()
        a = self.shadow[:,:,3]
        r,g,b = cv2.split(new_mask)
        new_mask = cv2.merge((r,g,b,a))
        self.perlin_mask = new_mask
        self.shadow = self.apply(new_mask)



