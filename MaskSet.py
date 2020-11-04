import random
import cv2
import queue as que
import threading
import time
import file_tools as file_tools
import image_tools as image_tools
import perlin_noise as perlin_noise
from console_tools import print_progress_bar
from SilhouetteMask import SilhouetteMask
from PerlinMask import PerlinMask

class MaskSet:
    def __init__(self, largest_shape=(1024,1024), load=False):
        self.largest_shape = largest_shape
        self.silhouettes_path = file_tools.ps_he_tb
        self.silhouette_mask_path = file_tools.silhouette_masks_path
        self.perlin_mask_path = file_tools.perlin_masks_path
        if load:
            self.silhouette_mask_set = self.load_masks("Silhouette Masks", self.silhouette_mask_path)
            self.perlin_mask_set = self.load_masks("Perlin Masks", self.perlin_mask_path)
        else:
            self.silhouette_mask_set = self.init_silhouette_masks()
            self.perlin_mask_set = self.init_perlin_masks()
        self.mask_set = self.silhouette_mask_set + self.perlin_mask_set
        
    # Load mask images from directory
    def load_masks(self, type, directory):
        start = time.time() # Start timer
        mask_set = []
        # Get silhouette mask images path
        mask_path_list = file_tools.directory_image_list(directory)
        # Initialize progress bar
        progress_bar_prefix = "Loading " + type
        print_progress_bar(start, 0, len(mask_path_list), prefix=progress_bar_prefix, suffix="Complete", length=50)
        # Load silhouette masks
        for i, mask_path in enumerate(mask_path_list):
            # Start thread and wait for completion
            queue = que.Queue()
            thread = threading.Thread(
                target = lambda q, path: q.put(image_tools.load_image(path)),
                args = (queue, mask_path)
            )
            mask_image = image_tools.load_image(mask_path)
            if type == "Silhouette Masks":
                mask = SilhouetteMask(mask_image)
            elif type == "Perlin Masks":
                mask = PerlinMask(mask_image)
            # Update progress bar
            print_progress_bar(start, i+1, len(mask_path_list), prefix=progress_bar_prefix, suffix="Complete", length=50)
            mask_set.append(mask)
        return mask_set

    # Initialize silhouette masks
    def init_silhouette_masks(self):
        start = time.time() # Start timer
        # Get silhouette image paths
        silhouette_path_list = file_tools.directory_image_list(self.silhouettes_path)
        # Initialize silhouette mask set
        silhouette_mask_set = []
        # Number of different masks for each silhouette
        n = 3
        # Total number of silhouette masks
        silhouette_mask_set_length = len(silhouette_path_list) * n
        # Creates silhouette mask from given silhouette with randomized variables and returns
        def create_silhouette_mask(silhouette):
            transparency = random.uniform(0.4, 0.7)
            scale = random.randint(400,600)
            silhouette_mask = SilhouetteMask(silhouette)
            silhouette_mask.add_noise()
            silhouette_mask.blur()
            silhouette_mask.scale(scale)
            silhouette_mask.change_transparency(transparency)
            return silhouette_mask
        # Create silhouette mask set
        count = 0
        for silhouette_path in silhouette_path_list:
            silhouette = image_tools.load_image(silhouette_path)
            # Creates 3 different masks for each silhouette with randomized features
            for i in range(3):
                count += 1
                # Create thread and wait for completion
                queue = que.Queue()
                thread = threading.Thread(
                    target = lambda q, sil: q.put(create_silhouette_mask(sil)),
                    args=(queue, silhouette)
                )
                thread.start()
                thread.join()
                silhouette_mask = queue.get()
                silhouette_mask_set.append(silhouette_mask)
                # Update progress bar
                print_progress_bar(start, count, silhouette_mask_set_length, prefix="Silhouette Masks initialized:", suffix="Complete", length=50)
        return silhouette_mask_set

    # Initialize perlin masks
    def init_perlin_masks(self):
        # Start timer
        start = time.time()
        # Initialize perlin mask set
        perlin_mask_set = []
        # Get number of silhouette masks (same number of perlin masks)
        silhouette_mask_set_length = len(self.silhouette_mask_set)
        # Creates perlin mask
        def create_perlin_mask():
            perlin_mask = PerlinMask(shape=self.largest_shape)
            return perlin_mask
        # Create progress bar
        print_progress_bar(start, 0, silhouette_mask_set_length, prefix="Perlin Masks initialized:", suffix="Complete", length=50)
        # Create perlin mask set
        for i in range(silhouette_mask_set_length):
            # Create thread and wait for completion
            queue = que.Queue()
            thread = threading.Thread(
                target = queue.put(create_perlin_mask()),
                args = (queue)
            )
            thread.start()
            thread.join()
            perlin_mask = queue.get()
            perlin_mask_set.append(perlin_mask)
            # Update progress bar
            print_progress_bar(start, i+1, silhouette_mask_set_length, prefix="Perlin Masks:", suffix="Complete", length=50)
        return perlin_mask_set

    # Applies all masks to given image and return set
    def apply_masks(self, image):
        masked_image_set = []
        # Applies single mask to image and converts to gray 
        def apply_mask(image):
            masked_image = mask.apply(image)
            masked_image = cv2.cvtColor(masked_image, cv2.COLOR_RGB2GRAY)
            return masked_image
        # Apply silhouette masks
        # Start timer
        start = time.time()
        # Create progress bar
        print_progress_bar(start, 0, len(self.silhouette_mask_set), prefix="Applied silhouette masks:", suffix="Complete", length=50)
        for i, mask in enumerate(self.silhouette_mask_set):
            # Create thread and wait for completion
            queue = que.Queue()
            thread = threading.Thread(
                target = lambda q, img: q.put(apply_mask(img)),
                args = (queue, image)
            )
            thread.start()
            thread.join()
            masked_image = queue.get()
            masked_image_set.append(masked_image)
            # Update progress bar
            print_progress_bar(i+1, len(self.silhouette_mask_set), prefix="Applied silhouette masks:", suffix="Complete", length=50)
        # Apply perlin masks
        # Start timer
        start = time.time()
        # Create progress bar
        print_progress_bar(start, 0, len(self.perlin_mask_set), prefix="Applied silhouette masks:", suffix="Complete", length=50)
        for i, mask in enumerate(self.perlin_mask_set):
            # Create thread and wait for completion
            queue = que.Queue()
            thread = threading.Thread(
                target = lambda q, img: q.put(apply_mask(img)),
                args = (queue, image)
            )
            thread.start()
            thread.join()
            masked_image = queue.get()
            masked_image_set.append(masked_image)
            # Update progress bar
            print_progress_bar(start, i+1, len(self.perlin_mask_set), prefix="Applied silhouette masks:", suffix="Complete", length=50)
        return masked_image_set
            
    def save_masks(self):
        # Start timer
        start = time.time() 
        # Start progress bar
        print_progress_bar(start, 0, len(self.silhouette_mask_set), prefix="Saved silhouette masks:", suffix="Complete", length=50)
        for i, mask in enumerate(self.silhouette_mask_set):
            mask_path = self.silhouette_mask_path + "/silhouette_mask" + str(i) + ".png"
            # Create thread and wait for completion
            thread = threading.Thread(
                target = file_tools.save_image,
                args = (mask_path, mask.mask)
            )
            thread.start()
            thread.join()
            # Update progress bar
            print_progress_bar(start, i+1, len(self.silhouette_mask_set), prefix="Saved silhouette masks:", suffix="Complete", length=50)
        # Start timer
        start = time.time() 
        # Start progress bar
        print_progress_bar(start, 0, len(self.perlin_mask_set), prefix="Saved perlin masks:", suffix="Complete", length=50)
        for i, mask in enumerate(self.perlin_mask_set):
            mask_path = self.perlin_mask_path + "/perlin_mask" + str(i) + ".png"
            # Create thread and wait for completion
            thread = threading.Thread(
                target = file_tools.save_image,
                args = (mask_path, mask.mask)
            )
            thread.start()
            thread.join()
            # Update progress bar
            print_progress_bar(start, i+1, len(self.perlin_mask_set), prefix="Saved perlin masks:", suffix="Complete", length=50)
    