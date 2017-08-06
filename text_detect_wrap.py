#!/usr/bin/python

import sys
from text_detect.io_handler import IoHandler
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger
from text_detect.rectangle_selector import RectangleSelector as Selector


def detect_text_area(io_handler):
    # Load image
    img = io_handler.read_image()
    if img is None:
        raise FileNotFoundError
    # Detect text area
    detector = Detector()
    rectangles = detector.find_all_text_rectangles(img)
    if len(rectangles) == 0:
        print("[Warning] Not text rectangle detected !!")
    # Merge rectangles
    merger = Merger()
    rectangles = merger.merge_rectangle_list(rectangles)
    # Select rectangles
    selector = Selector()
    rectangles = selector.select_according_to_merged_times_and_area(rectangles)
    # Save result
    io_handler.write_result(img, rectangles)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        IoHandler.print_help_and_quit()
    ioHandler = IoHandler(sys.argv[1], (len(sys.argv) > 2) and './' or sys.argv[2])
    try:
        detect_text_area(ioHandler)
    except FileNotFoundError:
        print("File %s not exist !!" % ioHandler.input_file)
