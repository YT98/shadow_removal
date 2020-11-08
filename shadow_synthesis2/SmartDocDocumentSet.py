import os
import multiprocessing

import tools.file_tools as file_tools
from shadow_synthesis2.SmartDocDocument import SmartDocDocument

class SmartDocDocumentSet:
    def __init__(self):
        self.smartdoc_path = file_tools.smart_doc_documents_path
        self.document_set = self.init_document_set()
        self.no_shadow_docs, self.shadow_docs = self.split_set()

    def get_document_paths(self):
        document_paths = []
        for filename in os.listdir(self.smartdoc_path):
            # Ignore hidden files
            if not filename.startswith('.'):
                file_path = os.path.join(self.smartdoc_path, filename)
                document_paths.append(file_path)
        return document_paths

    def init_document(self, path):
        doc = SmartDocDocument(path)
        # Only return documents with
        # - No motion blur
        # - No out of focus blur
        # - Light conditions: night + table lamp night or table lamp night + object shadow
        # - Lateral incidence angle = Logintudinal incidence angle = 0
        if (doc.motion_blur == 0 and doc.out_of_focus_blur == 0 and 
            (doc.light_condition == 1 or doc.light_condition == 4) and
            doc.lateral_incidence_angle == 0 and doc.longitudinal_incidence_angle == 0):
            return SmartDocDocument(path)

    def init_document_set(self):
        print("Initializing SmartDocDocumentSet...")
        document_paths = self.get_document_paths()
        pool = multiprocessing.Pool()
        document_set = pool.map(self.init_document, document_paths)
        pool.close()
        document_set = list(filter(None, document_set))
        print("SmartDocDocumentSet Initialized.")
        return document_set

    # Splits set into shadow and no-shadow documents
    def split_set(self):
        no_shadow_docs = []
        shadow_docs = []
        for doc in self.document_set:
            if doc.light_condition == 1:
                no_shadow_docs.append(doc)
            if doc.light_condition == 4:
                shadow_docs.append(doc)
        return (no_shadow_docs, shadow_docs)
