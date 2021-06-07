# -*- coding: utf-8 -*-
from flask import Flask, Response

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    return Response("<h1>Flask</h1><p>You visited: /%s</p>"
                        % (path), mimetype="text/html")
