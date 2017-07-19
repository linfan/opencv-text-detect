import cv2
import os


class IoHandler:
    def __init__(self):
        self.input_file = None
        self.output_path = None

    def parse_param(self, argv):
        if len(argv) < 2:
            raise IndexError
        self.input_file = argv[1]
        if len(argv) > 2:
            self.output_path = argv[2].endswith('/') and argv[2] or "%s/" % argv[2]
        else:
            self.output_path = "./"

    def print_help_and_quit(self):
        print(' (ERROR) You must call this script with an argument (path_to_image_to_be_processed)\n')
        quit()

    def create_folder_if_not_exist(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def read_image(self):
        return cv2.imread(self.input_file)

    def write_result(self, img, rectangles):
        # Mark rectangles
        self.create_folder_if_not_exist(self.output_path)
        for i in range(0, len(rectangles)):
            r = rectangles[i]
            roi = img[r.y1:r.y2, r.x1:r.x2]
            cv2.imwrite("%spart-%02d.jpg" % (self.output_path, i), roi)
            cv2.rectangle(img, (r.x1, r.y1), (r.x2, r.y2), (0, 0, 0), 2)
            cv2.rectangle(img, (r.x1, r.y1), (r.x2, r.y2), (255, 255, 255), 1)
        cv2.imwrite("%sresult.jpg" % self.output_path, img)
