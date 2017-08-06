import cv2
import numpy as np
import os
from text_detect.rectangle import Rectangle


class RectangleDetector:
    """
    Extremal Region Filter Algorith
    Based on Neumann L., Matas J.: Real-Time Scene Text Localization and Recognition, CVPR 2012
    """

    def __init__(self):
        self.horizontal_only = True
        self.thresholdDelta = 10
        self.detectArea = [(0.00002, 0.002), (0.0002, 0.02), (0.002, 0.2)]
        self.minProbability1 = 0.99
        self.nonMaxSuppression = True
        self.minProbabilityDiff = 0.99
        self.minProbability2 = 0.99

    def _get_current_file_path(self):
        return os.path.split(os.path.realpath(__file__))[0]

    def _text_detect(self, img, channel, area_size_index=0):
        pathname = self._get_current_file_path()
        erc1 = cv2.text.loadClassifierNM1(pathname + '/cfg/trained_classifierNM1.xml')
        er1 = cv2.text.createERFilterNM1(erc1, self.thresholdDelta,
                                         self.detectArea[area_size_index][0], self.detectArea[area_size_index][1],
                                         self.minProbability1, self.nonMaxSuppression, self.minProbabilityDiff)
        erc2 = cv2.text.loadClassifierNM2(pathname + '/cfg/trained_classifierNM2.xml')
        er2 = cv2.text.createERFilterNM2(erc2, self.minProbability2)
        regions = cv2.text.detectRegions(channel, er1, er2)
        rects = []
        try:
            if self.horizontal_only:
                rects = cv2.text.erGrouping(img, channel, [r.tolist() for r in regions])
            else:
                rects = cv2.text.erGrouping(img, channel, [x.tolist() for x in regions],
                                           cv2.text.ERGROUPING_ORIENTATION_ANY,
                                           pathname + '/cfg/trained_classifier_erGrouping.xml', 0.9)
        except cv2.error:
            print('No rectangle detected !!!')
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
            for s in (0, 1, 2):
                rects = self._text_detect(img, channel, s)
                for r in range(0, np.shape(rects)[0]):
                    rectangles.append(Rectangle(rects[r]).set_area_size_index(s))
        return rectangles
