import multiprocessing
import tqdm

import tools.file_tools as file_tools
from shadow_synthesis.Document import Document

class DocumentSet:
    def __init__(self, smart_doc_documents):
        self.documents_path = file_tools.scanned_documents_path
        self.document_set = self.init_document_set()
        self.document_set += smart_doc_documents
        self.largest_shape = self.get_largest_shape()

    # Initializes documents set
    def init_document_set(self):
        print("Initializing DocumentSet...")
        documents_path_list = file_tools.directory_image_list(self.documents_path)
        pool = multiprocessing.Pool()
        document_set = list(tqdm.tqdm(pool.imap(Document, documents_path_list), total=len(documents_path_list)))
        return document_set

    # Returns document shape
    def get_shape(self, doc):
        image = doc.load_image()
        h, w, *_ = image.shape
        return [h, w]

    # Returns largest width and largest height in document set
    def get_largest_shape(self):
        print("Getting largest document shape...")
        pool = multiprocessing.Pool()
        shape_set = list(tqdm.tqdm(pool.imap(self.get_shape, self.document_set), total=len(self.document_set)))
        pool.close()
        largest_h = max(shape_set, key=lambda x: x[0])
        largest_w = max(shape_set, key=lambda x: x[1])
        return (largest_h, largest_w)