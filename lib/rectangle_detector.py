import cv2
import numpy as np
import os
import sys
from lib.rectangle import Rectangle


class RectangleDetector:
    """
    Extremal Region Filter Algorith
    Based on Neumann L., Matas J.: Real-Time Scene Text Localization and Recognition, CVPR 2012
    """

    def __init__(self):
        self.horizontal_only = True
        self.thresholdDelta = 30
        self.minArea = 0.00015
        self.maxArea = 0.2
        self.minProbability1 = 0.2
        self.nonMaxSuppression = True
        self.minProbabilityDiff = 0.2
        self.minProbability2 = 0.9

    def _text_detect(self, img, channel):
        pathname = os.path.dirname(sys.argv[0])
        erc1 = cv2.text.loadClassifierNM1(pathname + 'lib/cfg/trained_classifierNM1.xml')
        er1 = cv2.text.createERFilterNM1(erc1, self.thresholdDelta, self.minArea, self.maxArea,
                                         self.minProbability1, self.nonMaxSuppression, self.minProbabilityDiff)
        erc2 = cv2.text.loadClassifierNM2(pathname + 'lib/cfg/trained_classifierNM2.xml')
        er2 = cv2.text.createERFilterNM2(erc2, self.minProbability2)
        regions = cv2.text.detectRegions(channel, er1, er2)
        if self.horizontal_only:
            return cv2.text.erGrouping(img, channel, [r.tolist() for r in regions])
        else:
            return cv2.text.erGrouping(img, channel, [x.tolist() for x in regions],
                                       cv2.text.ERGROUPING_ORIENTATION_ANY,
                                       pathname + 'lib/cfg/trained_classifier_erGrouping.xml', 0.9)

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
            rects = self._text_detect(img, channel)
            for r in range(0, np.shape(rects)[0]):
                rectangles.append(Rectangle(rects[r]))
        return rectangles
