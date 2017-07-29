#!/usr/bin/python

import sys
from text_detect.io_handler import IoHandler
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger
from text_detect.rectangle_selector import RectangleSelector as Selector

io_handler = IoHandler()
try:
    io_handler.parse_param(sys.argv)
except IndexError:
    io_handler.print_help_and_quit()

# Load image
img = io_handler.read_image()

# Detect text area
detector = Detector()
rectangles = detector.find_all_text_rectangles(img)

# Merge rectangles
merger = Merger()
rectangles = merger.merge_rectangle_list(rectangles)

# Select rectangles
selector = Selector()
rectangles = selector.select_according_to_merged_times(rectangles)

# Save result
io_handler.write_result(img, rectangles)
