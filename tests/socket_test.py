# -*- coding: utf-8 -*-

import socket

client = socket.socket()
host = 'lab.csgowiki.top'
port = 50000

client.connect((host, port))
msg = "测试哦"
client.send(msg.encode('utf-8'))
print(client.recv(1024))
client.close()
