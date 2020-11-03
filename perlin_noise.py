import cv2
import noise
import numpy as np
from image_tools import show_image
import random

def perlin_mask(shape, scale, octaves, persistence, lacunarity, base):
    mask = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            # Value is normalized between -1 and 1
            pixel = noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=shape[0], 
                                        repeaty=shape[1], 
                                        base=base)
            # Denormalize between 0 and 255
            mask[i][j] = ((pixel+1)/2.0*255.0)
    # Cast float64 array to uint8
    mask = mask.astype(np.uint8)
    # Converting to RGB
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    return mask