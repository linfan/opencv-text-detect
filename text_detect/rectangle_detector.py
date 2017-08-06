import cv2
import numpy as np
import os
from text_detect.rectangle import Rectangle
from text_detect.detection_parameter import DetectionParameter


class RectangleDetector:
    """
    Extremal Region Filter Algorith
    Based on Neumann L., Matas J.: Real-Time Scene Text Localization and Recognition, CVPR 2012
    """

    def __init__(self):
        self.detection_parameter_list = [DetectionParameter(True, 3, 0.00002, 0.002, 0.9, True, 0.9, 0.9),
                                         DetectionParameter(True, 3, 0.0001, 0.02, 0.9, True, 0.9, 0.9),
                                         DetectionParameter(True, 3, 0.001, 0.2, 0.9, True, 0.9, 0.9)]

    def _get_current_file_path(self):
        return os.path.split(os.path.realpath(__file__))[0]

    def _text_detect(self, img, channel, area_size_index=0):
        para = self.detection_parameter_list[area_size_index]
        pathname = self._get_current_file_path()
        erc1 = cv2.text.loadClassifierNM1(pathname + '/cfg/trained_classifierNM1.xml')
        er1 = cv2.text.createERFilterNM1(erc1, para.thresholdDelta, para.minArea, para.maxArea,
                                         para.minProbability1, para.nonMaxSuppression, para.minProbabilityDiff)
        erc2 = cv2.text.loadClassifierNM2(pathname + '/cfg/trained_classifierNM2.xml')
        er2 = cv2.text.createERFilterNM2(erc2, para.minProbability2)
        regions = cv2.text.detectRegions(channel, er1, er2)
        rects = []
        try:
            if para.horizontalOnly:
                rects = cv2.text.erGrouping(img, channel, [r.tolist() for r in regions])
            else:
                rects = cv2.text.erGrouping(img, channel, [x.tolist() for x in regions],
                                            cv2.text.ERGROUPING_ORIENTATION_ANY,
                                            pathname + '/cfg/trained_classifier_erGrouping.xml', 0.9)
        except cv2.error:
            print('Not An Error: No text rectangle detected...')  # OpenCV would print error here, but it's actually not
        return rects

    def find_all_text_rectangles(self, img):
        # Extract channels to be processed individually
        channels = cv2.text.computeNMChannels(img)
        # Append negative channels to detect ER- (bright regions over dark background)
        cn = len(channels) - 1
        for c in range(0, cn):
            channels.append((255 - channels[c]))
        # Apply the default cascade classifier to each independent channel (could be done in parallel)
        rectangles = []
        for channel in channels:
            for s in range(0, len(self.detection_parameter_list)):
                rects = self._text_detect(img, channel, s)
                for r in range(0, np.shape(rects)[0]):
                    rectangles.append(Rectangle(rects[r]).set_area_size_index(s))
        return rectangles
