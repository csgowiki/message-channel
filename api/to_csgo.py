# -*- coding: utf -*-
import os
import socket
import ujson
from flask import Flask, jsonify, request

app = Flask(__name__)


def create_socket():
    return socket.socket()


@app.route('/api/to_csgo', methods=['POST'])
def to_csgo_view():
    return jsonify({"status": "error"})


@app.route('/api/tcp_connect', methods=['POST'])
def connect_tcp():
    socket_container = os.getenv('SOCKET_CONTAINER')
    if not socket_container:
        socket_container = {}
    else:
        socket_container = ujson.loads(socket_container)
    sv_remark = request.form.get("sv_remark")
    sv_host = request.form.get("sv_host")
    qq_group = request.form.get("qq_group")

    success = False
    if qq_group in socket_container.keys():
        for value in socket_container[qq_group]:
            if value == [sv_remark, sv_host]:
                return jsonify({
                    "status": "warning",
                    "message": "tcp connect exist"
                })
        socket_container[qq_group].append((sv_remark, sv_host))
        success = True
    else:
        socket_container[qq_group] = [(sv_remark, sv_host)]
        success = True

    if success:
        os.environ['SOCKET_CONTAINER'] = ujson.dumps(socket_container)
        return jsonify({
            "status": "ok",
            "message": "[success] tcp connect created"
        })
    else:
        return jsonify({"status": "error"})


@app.route('/api/tcp_close', methods=['POST'])
def close_tcp():
    socket_container = os.getenv('SOCKET_CONTAINER')
    if not socket_container:
        socket_container = {}
    else:
        socket_container = ujson.loads(socket_container)
    sv_remark = request.form.get("sv_remark")
    sv_host = request.form.get("sv_host")
    qq_group = request.form.get("qq_group")

    if qq_group in socket_container.keys():
        for value in socket_container[qq_group]:
            if value == [sv_remark, sv_host]:
                socket_container[qq_group].remove([sv_remark, sv_host])
                os.environ['SOCKET_CONTAINER'] = ujson.dumps(socket_container)
                return jsonify({
                    "status": "ok",
                    "message": "[success] tcp connect closed"
                })

    return jsonify({
        "status": "warning",
        "message": "tcp connect not exist"
    })
