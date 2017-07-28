#!/usr/bin/python

from flask import Flask, render_template, send_from_directory, request
import urllib.request
import urllib.error
import socket
from text_detect.io_handler import IoHandler
from text_detect.rectangle_detector import RectangleDetector as Detector
from text_detect.rectangle_merger import RectangleMerger as Merger
from text_detect.rectangle_selector import RectangleSelector as Selector
import subprocess

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
    message = ''
    success = True

    saved_image_name = url.split('/')[-1]
    saved_image_path = '%s/%s' % (static_folder, saved_image_name)
    msg, suc = download_image(saved_image_path, url)
    message, success = update_msg_and_suc(message, msg, success, suc)

    saved_image_name_without_postfix = saved_image_name.split('.')[0]
    output_folder = '%s/%s/' % (static_folder, saved_image_name_without_postfix)
    result_image_url = detect_text_area(saved_image_path, output_folder)

    part_image_file = '%s/part-0%d.jpg' % (output_folder, 1)
    detect_res = subprocess.run(["tesseract", part_image_file, "stdout", "--oem", "1", "--psm", "13"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    message, success = update_msg_and_suc(message, detect_res.stderr, success, detect_res.returncode == 0)
    if success:
        message = detect_res.stdout

    return render_template('res.html', success=success, image=result_image_url, message=message)


def update_msg_and_suc(message, msg, success, suc):
    success &= suc
    if not suc:
        message += '<li>%s</li>' % msg
    return message, success


def download_image(saved_image_path, url):
    message = ''
    socket.setdefaulttimeout(3)
    try:
        urllib.request.urlretrieve(url, saved_image_path)
        success = True
    except (urllib.error.HTTPError, urllib.error.URLError):
        success = False
        message = 'Failed to download image %s' % url
    return message, success


def detect_text_area(input_file, output_path):
    # Load image
    io_handler = IoHandler()
    io_handler.input_file = input_file
    io_handler.output_path = output_path
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
    return '%s%sresult.jpg' % (request.url_root, io_handler.output_path)
