from flask import Flask, request, jsonify
from service import VIcsnf, NfdFace, NfdRoute, NFDStrategy

import json

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

""" VNF Related API: 
    Create
    Get VNF by name
    Delete CNF
""" 
@app.route('/createvnfs', methods=["PUT"])
def create_vnf():
    return jsonify(VIcsnf().create(request.form))

@app.route('/api/vnf_info/<namespace>/<vnf_name>', methods=["GET"])
def get_vnf(namespace, vnf_name):
    return jsonify(VIcsnf().get(namespace, vnf_name))

@app.route('/deletevnfs', methods=["PUT"])
def delete_vnf():
    return jsonify(VIcsnf().delete(request.form))

""" NDN Face Related API:
    Create
    Get Face list by IP
    Delte Face
"""
@app.route('/createfaces', methods=["PUT"])
def create_nfd_face():
    return jsonify(NfdFace().create(request.form))

@app.route('/api/facelist/<ip>', methods=["GET"])
def get_nfd_face(ip):
    return jsonify(NfdFace().get(ip))

@app.route('/deletefaces', methods=["PUT"])
def delete_nfd_face():
    return jsonify(NfdFace().delete(request.form))

""" NFD route Related API:
    Create
    Get Face by IP
"""

@app.route('/api/createroute', methods=["POST"])
def create_nfd_route():
    return jsonify(NfdRoute().create(request.form))

@app.route('/api/fiblist/<ip>', methods=["GET"])
def get_nfd_fib(ip):
    return jsonify(NfdRoute().get(ip))

""" NFD strategy Related API:
    Create
"""
@app.route('/api/strategylist/<ip>', methods=["GET"])
def get_nfd_stragegy(ip):
    return jsonify(NFDStrategy().get(ip))


if __name__ == '__main__':
    app.run()
