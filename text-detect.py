#!/usr/bin/python

from flask import Flask, render_template, send_from_directory, request
import urllib.request
import urllib.error
import socket
import os
import re
from text_detect.io_handler import IoHandler
import text_detect_wrap
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
    messages = []
    success = True

    saved_image_name = url.split('/')[-1]
    saved_image_path = '%s/%s' % (static_folder, saved_image_name)
    success, messages = download_image(saved_image_path, url, success, messages)

    saved_image_name_without_postfix = saved_image_name.split('.')[0]
    output_folder = '%s/%s' % (static_folder, saved_image_name_without_postfix)
    result_image_url = detect_text_area(saved_image_path, output_folder)

    part_image_files = ls_dir(output_folder, r'.*part-[0-9]+\.jpg')
    for part in part_image_files:
        success, messages = recognize_text(part, output_folder, success, messages)

    if success:
        part_txt_files = ls_dir(output_folder, r'.*part-[0-9]+\.txt')
        for part in part_txt_files:
            messages.append(read_recognized_txt(part, output_folder))

    return render_template('res.html', success=success, image=result_image_url, messages=messages)


def read_recognized_txt(part, output_folder):
    part_file_path = '%s/%s' % (output_folder, part)
    txt_fd = open(part_file_path)
    line = txt_fd.readline()  # just the first line
    txt_fd.close()
    return re.sub(r'^[^0-9a-zA-Z]*', '', re.sub(r'[^0-9a-zA-Z]*$', '', line))


def ls_dir(output_folder, pattern):
    return [f for f in os.listdir(output_folder) if re.match(pattern, f)]


def recognize_text(part, output_folder, success, messages):
    suc, msg = True, ''
    part_file_path = '%s/%s' % (output_folder, part)
    detect_txt_file_path = '%s/%s' % (output_folder, part.replace('.jpg', ''))
    if not os.path.exists('%s.txt' % detect_txt_file_path):
        detect_res = subprocess.run(["tesseract", part_file_path, detect_txt_file_path, "--oem", "1", "--psm", "13"],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        suc, msg = (detect_res.returncode == 0), detect_res.stderr
    return update_msg_and_suc(success, suc, messages, msg)


def update_msg_and_suc(success, suc, messages, msg):
    if not suc:
        messages.append(msg)
    return (success and suc), messages


def download_image(saved_image_path, url, success, messages):
    suc, msg = True, ''
    if not os.path.exists(saved_image_path):
        try:
            socket.setdefaulttimeout(3)
            urllib.request.urlretrieve(url, saved_image_path)
        except (urllib.error.HTTPError, urllib.error.URLError):
            suc, msg = False, 'Failed to download image %s' % url
    return update_msg_and_suc(success, suc, messages, msg)


def detect_text_area(input_file, output_path):
    if not os.path.exists('%s/result.jpg' % output_path):
        # Load image
        io_handler = IoHandler()
        io_handler.input_file = input_file
        io_handler.output_path = '%s/' % output_path
        text_detect_wrap.detect_text_area(io_handler)
    return '%s%s/result.jpg' % (request.url_root, output_path)
