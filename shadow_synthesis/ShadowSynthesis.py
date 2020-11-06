import os
import time
import cv2

import tools.file_tools as file_tools
from tools.console_tools import print_progress_bar

from shadow_synthesis.MaskSet import MaskSet
from shadow_synthesis.DocumentSet import DocumentSet

class ShadowSynthesis:
    def __init__(self, load=False):
        self.training_data_path = file_tools.training_data_path
        self.document_set = DocumentSet()
        self.mask_set = MaskSet(self.document_set.largest_shape, load=load)
        self.training_data = {}



    def create_training_data(self, batch_count):
        document_set = self.document_set.document_set
        mask_set = self.mask_set.mask_set

        # Create document image batches
        batch_length = len(document_set) // batch_count
        batch_set = []
        for batch_index in range(batch_count - 1):
            batch_start = batch_index * batch_length
            batch_end = (batch_index + 1) * batch_length
            batch_set.append(self.document_set.document_set[batch_start:batch_end])
        progress_bar_length = batch_length * len(mask_set)

        # Iterate over batches
        for batch_index, batch in enumerate(batch_set):
            # Start timer
            start = time.time()
            # Initialize progress bar
            count = 0
            print_progress_bar(start, count, progress_bar_length, prefix="Masked images created - batch {}".format(batch_index+1), suffix="Complete", length=50)
            # Create and save masked images
            for doc_batch_index, doc in enumerate(batch):
                doc_index = (batch_index * doc_batch_index) + doc_batch_index
                document_destination = os.path.join(self.training_data_path, "document_" + str(doc_index) + ".jpg")
                doc = cv2.cvtColor(doc, cv2.COLOR_GRAY2RGB)
                file_tools.save_image(document_destination, doc)
                for mask_index, mask in enumerate(self.mask_set.mask_set):
                    masked_document_destination = os.path.join(self.training_data_path, "document_" + str(doc_index) + "_mask_" + str(mask_index) + ".jpg")
                    masked_doc = mask.apply(doc)
                    file_tools.save_image(masked_document_destination, masked_doc)
                    # Update progress bar
                    count = (doc_batch_index * len(self.mask_set.mask_set)) + mask_index
                    print_progress_bar(start, count, progress_bar_length, prefix="Masked images created - batch {}".format(batch_index+1), suffix="Complete", length=50)
