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
saved_image_folder = '%s/data' % static_folder
short_url_prefix = 'p'
app = Flask(__name__, template_folder=static_folder, static_url_path='/%s' % static_folder)


@app.route('/%s/<path:url>' % short_url_prefix)
def send_js(url):
    return send_from_directory(saved_image_folder, url)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/detect/<path:url>")
def hello(url):
    messages = []
    success = True
    result_image_url = ''

    saved_image_name = url.split('/')[-1]
    saved_image_path = '%s/%s' % (saved_image_folder, saved_image_name)
    success, messages = download_image(saved_image_path, url, success, messages)

    if success:
        saved_image_name_without_postfix = '.'.join(saved_image_name.split('.')[:-1])
        output_folder = '%s/%s' % (saved_image_folder, saved_image_name_without_postfix)
        try:
            result_image_url = detect_text_area(saved_image_path, output_folder) \
                .replace(saved_image_folder, short_url_prefix)
        except FileNotFoundError:
            success, messages = False, "The downloaded file %s is not an image" % saved_image_path

        if success:
            part_image_files = ls_dir(output_folder, r'.*part-[0-9]+\.jpg')
            for part in part_image_files:
                success, messages = recognize_text(part, output_folder, success, messages)

        if success:
            part_txt_files = ls_dir(output_folder, r'.*part-[0-9]+\.txt')
            for part in part_txt_files:
                messages.append(read_recognized_txt(part, output_folder))

    return render_template('res.html', success=success, messages=messages, image=result_image_url)


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
        except urllib.error.URLError as e:
            suc, msg = False, 'Failed to download image %s' % url + '. ' + e.__str__()
    return update_msg_and_suc(success, suc, messages, msg)


def detect_text_area(input_file, output_path):
    if not os.path.exists('%s/result.jpg' % output_path):
        io_handler = IoHandler(input_file, output_path)
        text_detect_wrap.detect_text_area(io_handler)
    return '%s%s/result.jpg' % (request.url_root, output_path)
