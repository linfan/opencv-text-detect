#!/usr/bin/python

from flask import Flask, render_template, send_from_directory, request
import urllib.request
import urllib.error
import socket
from text_detect.io_handler import IoHandler
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger
from text_detect.rectangle_selector import RectangleSelector as Selector

static_folder = 'static'
app = Flask(__name__, template_folder=static_folder, static_url_path='/%s' % static_folder)


@app.route('/p/<path:url>')
def send_js(url):
    return send_from_directory(static_folder, url)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/detect/<path:url>")
def hello(url):
    # Handle parameters
    image = '%s/new.png' % static_folder
    socket.setdefaulttimeout(3)
    try:
        urllib.request.urlretrieve(url, image)
        success = True
    except (urllib.error.HTTPError, urllib.error.URLError):
        success = False

    # Load image
    io_handler = IoHandler()
    io_handler.input_file = image
    io_handler.output_path = '%s/out/' % static_folder
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

    return render_template('res.html', success=success, root_url=request.url_root,
                           image=io_handler.output_path + 'result.jpg')
