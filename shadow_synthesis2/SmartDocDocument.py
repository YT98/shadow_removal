import cv2

from shadow_synthesis2.Document import Document

class SmartDocDocument(Document):
    def __init__(self, path):
        super().__init__(path)
        self.interpret_filename()

    # Override load_image
    def load_image(self):
        image = cv2.cvtColor(cv2.imread(self.path, cv2.IMREAD_UNCHANGED), cv2.COLOR_RGB2GRAY)
        return self.crop_image(image)

    # Get document attributes from filename
    def interpret_filename(self):
        # Get document parameters
        args = self.filename.split("_")
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

    # Find bounding rectangle and crops image
    def crop_image(self, image):
        # Apply threshold
        _, thresh = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv2.contourArea)
        # Get rectangle box points
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # Get rectangle dimensions
        width = int(rect[1][0])
        height = int(rect[1][1])
        # Get points for warping
        src_pts = box.astype("float32")
        dst_pts = np.array([
            [0, height-1],
            [0, 0],
            [width-1, 0],
            [width-1, height-1]
        ], dtype="float32")
        # Warp rotated rectangle
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(image, M, (width, height))
        # Crops 20 pixels to remove non-cropped pixels
        h, w, *_ = warped.shape
        roi = warped[20:h-20, 20:w-20]
        # Returns cropped and warped rectangle
        return roi