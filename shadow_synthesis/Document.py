import cv2

class Document:
    def __init__(self, path):
        self.path = path
        self.filename = self.get_filename(path)
        
    def get_filename(self, path):
        path_list = path.split("/")
        return path_list[len(path_list)-1]

    def load_image(self):
        image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    

