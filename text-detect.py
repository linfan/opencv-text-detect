#!/usr/bin/python

from flask import Flask, render_template, send_from_directory, request
import urllib.request

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
    image = '%s/new.png' % static_folder
    urllib.request.urlretrieve(url, image)
    success = True
    return render_template('res.html', success=success, root_url=request.url_root, image=image)

