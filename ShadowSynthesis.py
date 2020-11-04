import os
import time
import file_tools as file_tools
import cv2
from console_tools import print_progress_bar
from MaskSet import MaskSet
from DocumentSet import DocumentSet

class ShadowSynthesis:
    def __init__(self, load=False):
        self.training_data_path = file_tools.training_data_path
        self.document_set = DocumentSet()
        self.mask_set = MaskSet(self.document_set.largest_shape, load=load)
        self.training_data = {}

    def create_training_data(self):
        document_set = self.document_set.document_set
        mask_set = self.mask_set.mask_set
        training_data_length = len(document_set) * len(mask_set)
        # Start timer
        start = time.time()
        # Initialize progress bar
        print_progress_bar(start, 0, training_data_length, prefix="Masked images created", suffix="Complete", length=50)
        count = 0
        # Create and save masked images
        for doc_index, doc in enumerate(self.document_set.document_set):
            document_destination = os.path.join(self.training_data_path, "document_" + str(doc_index) + ".jpg")
            doc = cv2.cvtColor(doc, cv2.COLOR_GRAY2RGB)
            file_tools.save_image(document_destination, doc)
            for mask_index, mask in enumerate(self.mask_set.mask_set):
                masked_document_destination = os.path.join(self.training_data_path, "document_" + str(doc_index) + "_mask_" + str(mask_index) + ".jpg")
                masked_doc = mask.apply(doc)
                file_tools.save_image(masked_document_destination, masked_doc)
                # Update progress bar
                count += 1
                print_progress_bar(start, count, training_data_length, prefix="Masked images created", suffix="Complete", length=50)
