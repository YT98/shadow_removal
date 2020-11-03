import random
import cv2
import file_tools as file_tools
import image_tools as image_tools
import perlin_noise as perlin_noise

from SilhouetteMask import SilhouetteMask
from PerlinMask import PerlinMask

class MaskSet:
    def __init__(self):
        # TODO: Create console_tools
        print("INITIALIZING MASK SET")
        self.silhouettes_path = file_tools.ps_he_tb
        print("=========================")
        print("INITIALIZING SILHOUETTE MASK SET")
        self.silhouette_mask_set = self.init_silhouette_masks()
        print("Number of silhouette masks: ", len(self.silhouette_mask_set))
        print("=========================")
        print("INITIALIZING PERLIN MASK SET")
        self.perlin_mask_set = self.init_perlin_masks()
        print("Number of perlin masks: ", len(self.perlin_mask_set))
        print("=========================")
        self.mask_set = self.silhouette_mask_set + self.perlin_mask_set
        print("Number of masks in total: ", len(self.mask_set))
        print("=========================")
        
    def init_silhouette_masks(self):
        silhouette_path_list = file_tools.directory_image_list(self.silhouettes_path)
        silhouette_mask_set = []
        for silhouette_path in silhouette_path_list:
            silhouette = image_tools.load_image(silhouette_path)
            # Creates 3 different masks for each silhouette with randomized features
            for i in range(3):
                silhouette_mask = SilhouetteMask(silhouette)
                transparency = random.uniform(0.4, 0.8)
                scale = random.randint(200,300)
                silhouette_mask.add_noise()
                silhouette_mask.blur()
                silhouette_mask.scale(scale)
                silhouette_mask.change_transparency(transparency)
                silhouette_mask_set.append(silhouette_mask)
        return silhouette_mask_set

    def init_perlin_masks(self):
        perlin_mask_set = []
        for i in range(len(self.silhouette_mask_set)):
            perlin_mask = PerlinMask()
            perlin_mask_set.append(perlin_mask)
        return perlin_mask_set
    
    def apply_masks(self, image):
        shadowed_image_set = []
        for mask in self.mask_set:
            shadowed_image = mask.apply(image)
            shadowed_image = cv2.cvtColor(shadowed_image, cv2.COLOR_RGB2GRAY)
            shadowed_image_set.append(shadowed_image)
        return shadowed_image_set
            
                
    