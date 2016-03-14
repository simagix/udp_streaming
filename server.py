#! /usr/bin/env python

import json
import os
import subprocess
import sys
from flask import Flask, send_from_directory, request, Response
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

app = Flask(__name__)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
libraryRepo = 'library.repo'

library = [
    {'title': 'Demo', 'media': 'file:////home/pi/Videos/demo.mp4'}
]

processes = {}

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
    cmd = ['cvlc', '-v', file, '--sout', params]
    process = subprocess.Popen(cmd)
    tag = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.')))
    tag += '_'
    tag += str(port)
    print tag
    if processes.get(tag, 'none') != 'none':
        proc = processes[tag]
        proc.kill()
    processes[tag] = process
    return json.dumps({'ok': 1, 'ip': ip, 'port': port}), 201, {'Content-Type': 'application/json'}

@app.route('/ss/SetupSession', methods=['POST'])
def setupSession():
    root = ET.fromstring(request.data)
    ns = {'SetupSession': 'urn:com:comcast:ngsrm:2010:08:01'}
    tp = root.find('SetupSession:UnicastTransport', ns)
    ip = tp.get('destinationAddress')
    port = tp.get('destinationPort')
    # udpCast(ip, port, 0)
    result = ET.Element('SetupSessionResult')
    resp = ET.SubElement(result, 'Response')
    detail = ET.SubElement(result, 'StreamingResourceDetails')
    transport = ET.SubElement(detail, 'UnicastTransport')
    control = ET.SubElement(detail, 'StreamControlURL')
    return Response(tostring(result)), 200, {'Content-Type': 'application/xml'}

@app.route('/ss/TeardownSession', methods=['POST'])
def teardownSession():
    return "";

if __name__ == '__main__':
    if len(sys.argv) > 1:
        libraryRepo = sys.argv[1]
    print libraryRepo
    try:
        with open(libraryRepo, 'r') as repo:
            library = json.loads(repo.read())
    except:
        print 'error opening %s' % (libraryRepo)
    app.debug = True
    app.run(host= '0.0.0.0', port=5050)

