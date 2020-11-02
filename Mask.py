from image_tools import *
from file_tools import *
import cv2
import random

class Mask:
    def __init__(self, shadow):
        self.shadow = shadow
        self.shape = shadow.shape
    
    # Resizes shadow keeping its original aspect ratio
    def scale(self, scale):
        width = int(self.shape[1] * scale / 100)
        height = int(self.shape[0] * scale / 100)
        shape = (width, height)
        scaled = cv2.resize(self.shadow, shape, interpolation=cv2.INTER_AREA)
        self.shadow = np.asarray(scaled)
        self.shape = scaled.shape

    # Pads shadow with transparent pixels 
    # Returned image is of same shape as input image
    # Original shadow is always placed at the bottom but horizontal position is randomly determined
    def pad(self, image_shape):
        # TODO: Catch error if shadow is larger than img
        (img_h, img_w, _) = image_shape
        (shadow_h, shadow_w, _) = self.shape
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
        self.shape = padded.shape

    # Changes mask transparency
    def change_transparency(self, transparency):
        new_shadow = self.shadow.copy()
        a_channel_value = int(255*transparency)
        for x in range(new_shadow.shape[0]):
            for y in range(new_shadow.shape[1]):
                if (new_shadow[x, y, 3] != 0):
                    new_shadow[x, y, 3] = a_channel_value
        self.shadow = new_shadow

    # Applies mask to given image
    def apply(self, image):
        new_image = image.copy()
        # Normalize alpha channel from 0-255 to 0-1
        alpha = self.shadow[:,:,3] / 255.0
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * self.shadow[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image

    # Applies blurring to have a more realistic shadow
    def blur(self):
        # Pad shadow a little
        self.pad((self.shape[0]+50, self.shape[1]+50, 0))
        # Gaussian blur
        kernel_size = (15, 15)
        blurred = cv2.GaussianBlur(self.shadow, kernel_size, 15)
        self.shadow = blurred
        

