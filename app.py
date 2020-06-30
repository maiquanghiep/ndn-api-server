from flask import Flask, request, jsonify
from service import VIcsnf, NfdFace, NfdRoute, NFDStrategy, NLSR

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
@app.route('/createvnfs', methods=["POST"])
def create_vnf():
    return jsonify(VIcsnf().create(request.json))

@app.route('/api/vnf_info/<namespace>/<vnf_name>', methods=["GET"])
def get_vnf(namespace, vnf_name):
    return jsonify(VIcsnf().get(namespace, vnf_name))

@app.route('/deletevnfs', methods=["POST"])
def delete_vnf():
    return jsonify(VIcsnf().delete(request.json))

""" NDN Face Related API:
    Create
    Get Face list by IP
    Delte Face
"""
@app.route('/createfaces', methods=["PUT"])
def create_nfd_face():
    return jsonify(NfdFace().create(request.json))

@app.route('/api/facelist/<ip>', methods=["GET"])
def get_nfd_face(ip):
    return jsonify(NfdFace().get(ip))

@app.route('/deletefaces', methods=["PUT"])
def delete_nfd_face():
    return jsonify(NfdFace().delete(request.json))

""" NFD route Related API:
    Create
    Get Face by IP
"""

@app.route('/api/createroute', methods=["PUT"])
def create_nfd_route():
    return jsonify(NfdRoute().create(request.json))

@app.route('/api/deleteroute', methods=["PUT"])
def delete_nfd_route():
    return jsonify(NfdRoute().delete(request.json))

@app.route('/api/fiblist/<ip>', methods=["GET"])
def get_nfd_fib(ip):
    return jsonify(NfdRoute().get(ip))

""" NFD strategy Related API:
    Create
"""
@app.route('/api/strategyset', methods=["PUT"])
def set_strategy():
    return jsonify(NFDStrategy().create(request.json))
@app.route('/api/strategyunset', methods=["PUT"])
def unset_strategy():
    return jsonify(NFDStrategy().unset(request.json))
@app.route('/api/strategylist/<ip>', methods=["GET"])
def get_nfd_stragegy(ip):
    return jsonify(NFDStrategy().get(ip))


""" NLSR Related API:
    Create
"""
@app.route('/api/advertise', methods=["PUT"])
def nlsr_advertise():
    return jsonify(NLSR().advertise(request.json))
@app.route('/api/lsdb/<ip>', methods=["GET"])
def get_nlsr_lsdb(ip):
    return jsonify(NLSR().get(ip))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1010)
