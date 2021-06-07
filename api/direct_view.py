# -*- coding: utf-8 -*-
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/direct_channel', methods=['POST'])
def hello_world():
    resp = request.get_json()
    try:
        token = os.getenv('ACCESS_TOKEN')
        http_host = os.getenv('HTTP_HOST')
        qq_group = resp['qq_group']
        sv_remark = resp['sv_remark']
        message = resp['message']
        message = f"{sv_remark}:{message}".decode('utf-8')

        assert qq_group == '874734861'
        url = (
            f"{http_host}/send_group_msg?"
            f"group_id={qq_group}&"
            f"message={message}&"
            f"access_token={token}"
        )
        new_resp = requests.get(url)
        new_resp.raise_for_status()
        return jsonify({"status": "ok"})
    except Exception as ept:
        return jsonify({"status": "error", "message": ept})
