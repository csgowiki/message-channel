# -*- coding: utf-8 -*-
import os
import requests
import ujson
from flask import Flask, request, jsonify

app = Flask(__name__)


def decode_monitor_str(sv_remark: str, message: str) -> str:
    words = ujson.loads(message)
    if len(words) > 0 and isinstance(words[0], str):
        msg = (
            f"====玩家列表====\n服务器：{sv_remark}\n"
            f"当前地图：{words[0]}\n在线{len(words)-1}人"
        )
        words = words[1:]
    else:
        msg = f"====玩家列表====\n服务器：{sv_remark}\n在线0人"
    for word in words:
        msg += f"\n{word[0]}({word[2]}ms)"
    return msg


@app.route('/api/to_qq', methods=['POST'])
def direct_view():
    try:
        token = os.getenv('ACCESS_TOKEN')
        http_host = os.getenv('HTTP_HOST')
        qq_group = request.form.get('qq_group')
        sv_remark = request.form.get('sv_remark')
        sender = request.form.get('sender')
        message = request.form.get('message')
        msg_type = int(request.form.get('msg_type'))
        assert len(qq_group) != 0

        assert qq_group == '874734861'
        if msg_type == 0:
            message = f"[{sv_remark}]{sender}：{message}"
        elif msg_type == 1:
            message = decode_monitor_str(sv_remark, message)
        elif msg_type == 1:
            message = f"[{sv_remark}] {message}"

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
