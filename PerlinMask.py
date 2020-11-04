import numpy as np
import random
import cv2
from perlin_noise import perlin_mask

class PerlinMask:
    def __init__(self, shape, scale=200.0, octaves=4, lacunarity=2.0, base=1):
        self.shape = shape
        self.scale = scale
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.base = base
        self.persistence = random.uniform(0.0, 0.85)
        self.transparency = random.uniform(0.4, 0.8)
        self.mask = self.init_mask()

    # Creates mask
    def init_mask(self):
        mask = perlin_mask(
            self.shape, 
            self.scale, 
            self.octaves, 
            self.persistence, 
            self.lacunarity, 
            self.base
        )
        # Add alpha channel
        a = np.full((self.shape[0],self.shape[1],1), 255.0 * self.transparency, dtype=np.uint8)
        r, g, b = cv2.split(mask)
        mask = cv2.merge((r, g, b, a))
        return mask

    # Trims mask to given shape
    def trim(self, shape):
        h, w, *_ = self.mask.shape
        self.mask = self.mask[:h,:w,:]

    # Applies mask to given image
    def apply(self, image):
        # Apply mask to image
        new_image = image.copy()
        # Trim mask to image shape
        self.trim(image.shape)
        # Normalize alpha channel from 0-255 to 0-1
        alpha = self.mask[:,:,3] / 255.0
        # TODO try doing :3 instead of range(3)
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * self.mask[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image