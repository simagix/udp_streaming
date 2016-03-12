#! /usr/bin/env python

import json
import subprocess
from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route("/streaming/udp/<string:ip>/<int:port>", methods=["GET"])
def udpCast(ip, port):
    file = "file:////home/pi/Videos/skyfall.mp4"
    params = "#std{access=udp,mux=ts,dst="
    params += ip
    params += ":"
    params += str(port)
    params += "}"
    subprocess.Popen(["cvlc", "-v", file, "--sout", params])
    return json.dumps({}), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')

