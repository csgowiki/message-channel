# -*- coding: utf-8 -*-
from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    key = request.args.get('key')
    return Response("<h1>Flask</h1><p>You visited: /%s</p><p>key=%s</p>"
                        % (path, key), mimetype="text/html")
    return 'Hello World'


if __name__ == '__main__':
    app.run()
