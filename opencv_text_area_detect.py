#!/usr/bin/python

import sys
from text_detect.io_handler import IoHandler
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger

io_handler = IoHandler()
try:
    io_handler.parse_param(sys.argv)
except IndexError:
    io_handler.print_help_and_quit()

# Load image
img = io_handler.read_image()

# Detect text
detector = Detector()
rectangles = detector.find_all_text_rectangles(img)

# Merge rectangles
merger = Merger()
rectangles = merger.merge_rectangle_list(rectangles)

# Save result
io_handler.write_result(img, rectangles)
