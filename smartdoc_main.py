import os
import sys
import cv2

import tools.image_tools as image_tools
import tools.file_tools as file_tools

from smartdoc.Document import Document
from smartdoc.DocumentSet import DocumentSet

# Add tools to sys.path so shadow_synthesis directory files can access them
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, 'tools'))

if __name__ == '__main__':
    doc_set = DocumentSet()