import cv2
import noise
import numpy as np
from image_tools import show_image
import random

import matplotlib.pyplot as plt

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
    # Make whites whiter and black blacker
    minValue = np.amin(mask)
    mask = mask - minValue
    maxValue = np.amax(mask)
    mask = (mask / maxValue) * 255.0
    # Cast array to uint8
    mask = mask.astype(np.uint8)
    # Converting to RGB
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    return mask

mask = perlin_mask((1024,1024), 200.0, 4, 0.4, 2.0, 0)
show_image(mask)