from pathos.multiprocessing import ProcessingPool, ThreadingPool
import uuid
import cv2
import os
import tqdm
from itertools import product

import tools.file_tools as file_tools
import tools.image_tools as image_tools

from shadow_synthesis2.SmartDocDocumentSet import SmartDocDocumentSet
from shadow_synthesis2.DocumentSet import DocumentSet
from shadow_synthesis2.MaskSet import MaskSet

class ShadowSynthesis:
    def __init__(self, load_masks=False):
        self.training_data_path = file_tools.training_data_path
        self.smart_doc_set = SmartDocDocumentSet()
        self.doc_set = DocumentSet(self.smart_doc_set.no_shadow_docs)
        self.mask_set = MaskSet(self.doc_set.largest_shape, load=load_masks)

    def apply_masks(self, doc_image, doc_name, mask):
        mask.load_mask() # Load mask
        masked_image = mask.apply(doc_image) # Apply mask
        masked_name = doc_name + "_mask_" + str(uuid.uuid4()) # Name masked
        cv2.imwrite(masked_name + ".jpg", masked_image) # Save masked
        
    def apply_masks_unpack(self, args):
        return self.apply_masks(*args)

    def handle_document(self, document):
        doc_image = document.load_image() # Load doc
        doc_name = os.path.join(self.training_data_path, "doc_" + str(uuid.uuid4())) # Name doc
        cv2.imwrite(doc_name + ".jpg", doc_image) # Save doc
        # Apply masks
        return list(ProcessingPool().imap(self.apply_masks_unpack, product([doc_image], [doc_name], self.mask_set.mask_set)))

    def create_training_data(self):
        # Delete existing data
        for f in os.listdir(self.training_data_path):
            os.remove(os.path.join(self.training_data_path, f))
        # Create data
        print("Creating training data...")
        _ = list(tqdm.tqdm(ThreadingPool().imap(self.handle_document, self.doc_set.document_set), total=len(self.doc_set.document_set)))

