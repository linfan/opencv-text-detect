#!/usr/bin/python

import sys

import cv2
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger

if len(sys.argv) < 2:
    print(' (ERROR) You must call this script with an argument (path_to_image_to_be_processed)\n')
    quit()

# Load image
img = cv2.imread(str(sys.argv[1]))

# Detect text
detector = Detector()
rectangles = detector.find_all_text_rectangles(img)

# Merge rectangles
merger = Merger()
rectangles = merger.merge_rectangle_list(rectangles)

# Mark rectangles
for r in rectangles:
    cv2.rectangle(img, (r.x1, r.y1), (r.x2, r.y2), (0, 0, 0), 2)
    cv2.rectangle(img, (r.x1, r.y1), (r.x2, r.y2), (255, 255, 255), 1)

# Save result
cv2.imwrite("result.jpg", img)
