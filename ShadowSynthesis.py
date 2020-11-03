
from MaskSet import MaskSet
from DocumentSet import DocumentSet

class ShadowSynthesis:
    def __init__(self):
        self.document_set = DocumentSet()
        self.mask_set = MaskSet(self.document_set.largest_shape)
        


