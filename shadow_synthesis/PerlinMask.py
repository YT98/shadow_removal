import numpy as np
import random
import cv2

from tools.perlin_noise import perlin_mask

class PerlinMask:
    def __init__(self, mask=None, shape=None, scale=200.0, octaves=4, lacunarity=2.0):
        self.scale = scale
        self.octaves = octaves
        self.lacunarity = lacunarity
        self.base = random.randint(0,500)
        self.persistence = random.uniform(0.0, 0.85)
        self.transparency = random.uniform(0.4, 0.7)
        if shape != None:
            self.shape = shape
            self.mask = self.init_mask()
        elif mask.all() != None:
            self.mask = mask
            self.shape = self.mask.shape
        

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
        h, w, *_ = shape
        return self.mask[:h,:w,:]

    # Applies mask to given image
    def apply(self, image):
        # Apply mask to image
        new_image = image.copy()
        # Trim mask to image shape
        trimmed = self.trim(image.shape)
        # Normalize alpha channel from 0-255 to 0-1
        alpha = trimmed[:,:,3] / 255.0
        # TODO try doing :3 instead of range(3)
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * trimmed[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image