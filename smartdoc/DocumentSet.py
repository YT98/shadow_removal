import os
import multiprocessing
import cv2
import matplotlib.pyplot as plt

import tools.file_tools as file_tools
from smartdoc.Document import Document

class DocumentSet:
    def __init__(self):
        self.smartdoc_path = file_tools.smart_doc_images_path
        self.document_set = []
        self.init_document_set()

    def get_document_paths(self):
        document_paths = []
        for file in os.listdir(self.smartdoc_path):
            # Ignore hidden files
            if not file.startswith('.'):
                document_paths.append(file)
        return document_paths

    def init_document(self, path):
        doc = Document(path)
        if (doc.motion_blur == 0 and doc.out_of_focus_blur == 0 and doc.light_condition != 2 and
            doc.lateral_incidence_angle == 0 and doc.longitudinal_incidence_angle == 0):
            return Document(path)

    def init_document_set(self):
        document_paths = self.get_document_paths()
        pool = multiprocessing.Pool()
        document_set = pool.map(self.init_document, document_paths)
        pool.close()
        self.document_set = document_set
