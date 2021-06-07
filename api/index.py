# -*- coding: utf-8 -*-
import os
from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    access_token = os.getenv('access_token')
    return Response("<h1>Flask</h1><p>You visited: /%s</p>"
                        % (access_token), mimetype="text/html")

if __name__ == '__main__':
    app.run()
