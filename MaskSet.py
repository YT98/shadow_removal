import random
import cv2
import file_tools as file_tools
import image_tools as image_tools
import perlin_noise as perlin_noise

import queue as que
import threading
import time

from console_tools import print_progress_bar

from SilhouetteMask import SilhouetteMask
from PerlinMask import PerlinMask

class MaskSet:
    def __init__(self):
        print("Initializing mask set:")
        self.silhouettes_path = file_tools.ps_he_tb
        self.silhouette_mask_set = self.init_silhouette_masks()
        self.perlin_mask_set = self.init_perlin_masks()
        self.mask_set = self.silhouette_mask_set + self.perlin_mask_set
        
    # Initialize silhouette masks
    def init_silhouette_masks(self):
        # Start timer
        start = time.time()
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
            transparency = random.uniform(0.4, 0.8)
            scale = random.randint(200,300)
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
                print_progress_bar(count, silhouette_mask_set_length, prefix="Silhouette Masks:", suffix="Complete", length=50)

        # Print timer
        print("Timer: ", time.time() - start)
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
            perlin_mask = PerlinMask()
            return perlin_mask

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
            print_progress_bar(i+1, silhouette_mask_set_length, prefix="Perlin Masks:", suffix="Complete", length=50)

        # Print timer
        print("Timer: ", time.time() - start)
        return perlin_mask_set
    
    # Applies all masks to given image and return set
    def apply_masks(self, image):
        masked_image_set = []

        # Applies single mask to image and converts to gray 
        def apply_mask(image):
            masked_image = mask.apply(image)
            masked_image = cv2.cvtColor(masked_image, cv2.COLOR_RGB2GRAY)
            return masked_image

        # Create masked image set
        ##
        # Apply silhouette masks
        print("Applying silhouette masks:")
        # Start timer
        start = time.time()
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
        # Print timer
        print("Timer: ", time.time() - start)
        ##
        # Apply perlin masks
        print("Applying perlin masks:")
        # Start timer
        start = time.time()
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
            print_progress_bar(i+1, len(self.perlin_mask_set), prefix="Applied silhouette masks:", suffix="Complete", length=50)
        # Print timer
        print("Timer: ", time.time() - start)
        
        return masked_image_set
            
                
    