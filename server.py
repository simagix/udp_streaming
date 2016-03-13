#! /usr/bin/env python

import json
import os
import subprocess
from flask import Flask, send_from_directory, request

app = Flask(__name__)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

library = [
    {'title': 'Skyfall', 'media': 'file:////home/pi/Videos/skyfall.mp4'},
    {'title': 'Just The Way You Are', 'media': 'file:////home/pi/Videos/just_the_way_you_are.mp4'}
]

@app.route("/")
def redirec2index():
    return send_from_directory(root, 'index.html')

@app.route('/streaming/titles', methods=['GET'])
def getTitles():
    docs = []
    index = 0;
    for doc in library:
        docs.append({'title': doc['title'], 'index': index})
        index += 1
    return json.dumps(docs), 200, {'Content-Type': 'application/json'}

@app.route('/streaming/udp/<string:ip>/<int:port>/<int:index>', methods=['POST'])
def udpCast(ip, port, index):
    if ip == 'remote':
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    doc = library[index]
    file = doc['media']
    params = '#std{access=udp,mux=ts,dst='
    params += ip
    params += ':'
    params += str(port)
    params += '}'
    subprocess.Popen(['cvlc', '-v', file, '--sout', params])
    return json.dumps({'ok': 1, 'ip': ip, 'port': port}), 201, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')

