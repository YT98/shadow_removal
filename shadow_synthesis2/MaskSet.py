import os
import random
import multiprocessing
import tqdm

import tools.file_tools as file_tools

from shadow_synthesis2.SilhouetteMask import SilhouetteMask

class MaskSet:
    def __init__(self, largest_shape, load=False):
        self.largest_shape = largest_shape
        self.silhouettes_path = file_tools.ps_he_tb
        self.silhouette_masks_path = file_tools.silhouette_masks_path
        if load:
            # Populates self.mask_set
            self.load_silhouette_masks()
        else:
            # Saves and populates self.mask_set
            self.create_silhouette_masks()

    # TODO: Change "load" to something else

    # Load existing silhouette masks
    def load_silhouette_masks(self):
        print("Loading silhouette masks...")
        mask_paths = os.listdir(self.silhouette_masks_path)
        pool = multiprocessing.Pool()
        mask_list = list(tqdm.tqdm(pool.imap(self.load_silhouette_mask, mask_paths), total=len(mask_paths)))
        pool.close()
        self.mask_set = mask_list
    def load_silhouette_mask(self, path):
        mask = SilhouetteMask(mask_path=path)
        return mask

    # Create new silhouette masks
    def create_silhouette_masks(self):
        print("Creating and loading silhouette masks...")
        # Get silhouette paths
        silhouette_paths = file_tools.directory_image_list(self.silhouettes_path)
        # Delete already existing masks from directory
        for f in os.listdir(self.silhouette_masks_path):
            os.remove(os.path.join(self.silhouette_masks_path, f))
        # Create silhouette masks
        pool = multiprocessing.Pool()
        mask_list = list(tqdm.tqdm(pool.imap(self.create_silhouette_mask, silhouette_paths), total=len(silhouette_paths)))
        pool.close()
        self.mask_set = mask_list
    def create_silhouette_mask(self, silhouette_path):
        mask = SilhouetteMask(silhouette_path=silhouette_path)
        mask.add_noise()
        mask.blur()
        mask.scale(random.randint(200, 500))
        mask.change_transparency(random.uniform(0.4, 0.7))
        mask.save_mask()
        return mask