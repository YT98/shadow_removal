import numpy as np
import random
import cv2
from perlin_noise import perlin_mask

class PerlinMask:
    def __init__(self):
        self.scale = 100.0
        self.octaves = 4
        self.lacunarity = 3.0
        self.base = 1
        self.persistence = random.uniform(0.05, 0.25)
        self.transparency = random.uniform(0.4, 0.8)

    # Creates mask of given shape
    def init_mask(self, shape):
        # Create mask
        w, h, *_ = shape
        mask = perlin_mask(
            (w, h), 
            self.scale, 
            self.octaves, 
            self.persistence, 
            self.lacunarity, 
            self.base
        )
        # Add alpha channel
        a = np.full((w,h,1), 255.0 * self.transparency, dtype=np.uint8)
        r, g, b = cv2.split(mask)
        mask = cv2.merge((r, g, b, a))
        return mask

    # Applies mask to given image
    def apply(self, image):
        # Initialize mask with given shape
        self.mask = self.init_mask(image.shape)
        # Apply mask to image
        new_image = image.copy()
        # Normalize alpha channel from 0-255 to 0-1
        alpha = self.mask[:,:,3] / 255.0
        # TODO try doing :3 instead of range(3)
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * self.mask[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image
        
        


        