import os
import cv2

import tools.file_tools as file_tools

class Document:
    def __init__(self, path):
        self.path = path
        self.interpret_path()

    def interpret_path(self):
        # Get document parameters
        args = self.path.split("_")
        # Remove ".jpg" from last argument
        args[len(args)-1] = args[len(args)-1][:-4]
        # Set Document attributes
        self.distortions = args[0] # M or S
        self.document_number = int(args[3][1:]) # D1
        self.light_condition = int(args[4][1:]) # L1
        self.distance = int(args[5][1:]) # r35
        self.longitudinal_incidence_angle = int(args[6][1:]) # a20
        self.lateral_incidence_angle = int(args[7][1:]) # b10
        if len(args)-1 > 7:
            last_arg = args[8]
            self.motion_blur = args[8][2:] if (args[8][:2] == "Mb") else 0 # Mb1
            self.out_of_focus_blur = args[8][2:] if (args[8][:2] == "Ob") else 0 # Ob1
        else:
            self.motion_blur = self.out_of_focus_blur = 0

    def load_image(self):
        image_path = os.path.join(file_tools.smart_doc_images_path, self.path)
        self.image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)