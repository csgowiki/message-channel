# -*- coding: utf -*-
import socket
from flask import Flask, jsonify, request

app = Flask(__name__)

socket_cotainer = {}


def create_socket():
    return socket.socket()


@app.route('/api/to_csgo', methods=['POST'])
def to_csgo_view():
    return jsonify({"status": "error"})


@app.route('/api/tcp_connect', methods=['POST'])
def connect_tcp():
    global socket_container
    sv_remark = request.form.get("sv_remark")
    qq_group = request.form.get("qq_group")
    token = request.form.get("token")

    if (qq_group, sv_remark) in socket_container.keys():
        return jsonify({"status": "warning", "message": "tcp connect exist"})
    else:
        socket_container[(qq_group, sv_remark)] = create_socket()
        return jsonify({"status": "ok", "message": "created a tcp connect"})
    return jsonify({"status": "error"})


@app.route('/api/tcp_close', methods=['POST'])
def close_tcp():
    global socket_container
    sv_remark = request.form.get("sv_remark")
    qq_group = request.form.get("qq_group")
    token = request.form.get("token")

    if (qq_group, sv_remark) in socket_container.keys():
        del socket_container[(qq_group, sv_remark)]
        return jsonify({"status": "ok", "message": "closed a tcp connect"})
    else:
        return jsonify({"status": "warning", "message": "no exist tcp connect"})
    return jsonify({"status": "error"})
