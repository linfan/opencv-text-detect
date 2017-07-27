#!/usr/bin/python

from flask import Flask

app = Flask(__name__)


@app.route("/detect/<path:image>")
def hello(image=None):
    return "Detect Text in %s" % image

