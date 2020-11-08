import cv2
import random
import uuid

import tools.file_tools as file_tools
from tools.perlin_noise import *

class SilhouetteMask:
    def __init__(self, silhouette_path=None, mask_path=None):
        if mask_path == None:
            self.path = silhouette_path
            self.load_mask()
        else:
            self.path = mask_path
            # self.mask = self.load_mask(mask_path)

    # Loads mask image
    def load_mask(self):
        mask = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        self.mask = mask

    # Saves created silhouette mask
    def save_mask(self):
        save_path = file_tools.silhouette_masks_path + "/" + str(uuid.uuid4()) + ".png"
        cv2.imwrite(save_path, self.mask)
        self.path = save_path

    # Applies mask to given image
    def apply(self, image):
        padded = self.pad(image.shape)
        new_image = image.copy()
        # Normalize alpha channel from 0-255 to 0-1
        alpha = padded[:,:,3] / 255.0
        # TODO try doing :3 instead of range(3)
        # Element-wise multiplication, each channel multiplied by alpha (or 1-alpha)
        for color in range(3):
            new_image[:,:,color] = alpha * padded[:,:,color] + (1-alpha) * new_image[:,:,color]
        return new_image

    # Resizes mask keeping its original aspect ratio
    def scale(self, scale):
        width = int(self.mask.shape[1] * scale / 100)
        height = int(self.mask.shape[0] * scale / 100)
        shape = (width, height)
        scaled = cv2.resize(self.mask, shape, interpolation=cv2.INTER_AREA)
        self.mask = np.asarray(scaled)

    # Trims given number of pixels from mask
    def cut(self, top, bottom, left, right):
        h,w,*_ = self.mask.shape
        cut_mask = self.mask[top : h-bottom, left : w-right, :]
        return cut_mask

    # Pads mask with transparent pixels 
    # Returned image is of same shape as input image
    # Original mask is always placed at the bottom but horizontal position is randomly determined
    def pad(self, image_shape):
        # Unpack shapes
        (img_h, img_w, *_) = image_shape
        (mask_h, mask_w, *_) = self.mask.shape
        # Check mask / image dimensions
        if (mask_h >= img_h) and (mask_w >= img_w):
            trim_top = mask_h - img_h
            trim_left = random.randint(0, mask_w - img_w)
            trim_right = mask_w - img_w - trim_left
            padded = self.cut(trim_top, 0, trim_left, trim_right)
        elif (mask_h >= img_h) and (mask_w < img_w):
            trim_top = mask_h - img_h
            padding_left = random.randint(0, img_w - mask_w)
            padding_right = img_w - mask_w - padding_left
            padded = self.cut(trim_top, 0, 0, 0)
            padded = cv2.copyMakeBorder(
                padded, 
                0,
                0, 
                padding_left, 
                padding_right, 
                cv2.BORDER_CONSTANT, 
                value=[0,0,0,0]
            )
        elif (mask_h < img_h) and (mask_w >= img_w):
            padding_top = img_h - mask_h
            trim_left = random.randint(0, mask_w - img_w)
            trim_right = mask_w - img_w - trim_left
            padded = self.cut(0, 0, trim_left, trim_right)
            padded = cv2.copyMakeBorder(
                padded, 
                padding_top,
                0, 
                0, 
                0, 
                cv2.BORDER_CONSTANT, 
                value=[0,0,0,0]
            )
        else:
            padding_top = img_h - mask_h
            padding_left = random.randint(0, img_w - mask_w)
            padding_right = img_w - mask_w - padding_left
            padded = cv2.copyMakeBorder(
                self.mask, 
                padding_top,
                0, 
                padding_left, 
                padding_right, 
                cv2.BORDER_CONSTANT, 
                value=[0,0,0,0]
            )
        return padded

    # Changes mask transparency
    def change_transparency(self, transparency):
        new_mask = self.mask.copy()
        new_a = new_mask[:,:,3]
        new_a = np.array(new_a * transparency, dtype=np.uint8)
        r, g, b, old_a = cv2.split(new_mask)
        new_mask = cv2.merge((r,g,b,new_a))
        self.mask = new_mask

    # Applies gaussian blur to have a more realistic mask
    def blur(self):
        # Pad mask a little
        padded = self.pad((self.mask.shape[0]+50, self.mask.shape[1]+50, 0))
        # Gaussian blur
        kernel_size = (15, 15)
        blurred = cv2.GaussianBlur(padded, kernel_size, 15, borderType=cv2.BORDER_REPLICATE)
        self.mask = blurred
        
    # Adds gaussian noise to have a more realistic mask
    def add_noise(self):
        # Pad mask a little
        padded = self.pad((self.mask.shape[0]+50, self.mask.shape[1]+50, 0))
        self.mask = padded
        # Create perlin mask
        scale = 100.0
        octaves = 4
        lacunarity = 3.0
        base = 1
        persistence = random.uniform(0.05, 0.25)
        mask = perlin_mask(
            (padded.shape[0], padded.shape[1]), 
            scale, 
            octaves, 
            persistence, 
            lacunarity, 
            base
        )
        # Add alpha channel to perlin mask
        new_mask = mask.copy()
        a = padded[:,:,3]
        r,g,b = cv2.split(new_mask)
        new_mask = cv2.merge((r,g,b,a))
        self.mask = self.apply(new_mask)