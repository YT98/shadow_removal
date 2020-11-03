import sys
import file_tools as file_tools
import image_tools as image_tools

class DocumentSet:
    def __init__(self):
        self.documents_path = file_tools.scanned_documents_path
        self.document_set = self.init_document_set()
        self.largest_shape = self.get_largest_shape()

    # Initializes documents set
    def init_document_set(self):
        documents_path_list = file_tools.directory_image_list(self.documents_path)
        document_set = []
        for document_path in documents_path_list:
            document = image_tools.load_image(document_path)
            document_set.append(document)
        return document_set

    # Returns largest width and largest height in document set
    def get_largest_shape(self):
        largest_w = sys.maxsize
        largest_h = sys.maxsize
        for document in self.document_set:
            # Unpack document shape
            document_h, document_w, *_ = document.shape
            largest_h = document_h if (document_h > largest_h) else largest_h
            largest_w = document_w if (document_w > largest_w) else largest_w
        return (largest_h, largest_w)
