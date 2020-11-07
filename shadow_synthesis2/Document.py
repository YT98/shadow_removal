import cv2

class Document:
    def __init__(self, path):
        self.path = path
        self.get_filename = get_filename(path)
        
    def get_filename(self, path):
        path_list = path.split("/")
        return path_list[len(path_list)-1]

    def load_image(self):
        # Load and convert to grayscale
        self.image = cv2.cvtColor(cv2.imread(self.path, cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
        # self.image = self.crop_image(image)
    

