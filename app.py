from flask import Flask, request, jsonify
from service import VIcsnf, NfdFace, NfdRoute

import json

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/createvnfs', methods=["PUT"])
def create_vnf():
    return jsonify(VIcsnf().create(request.form))

@app.route('/deletevnfs', methods=["PUT"])
def delete_vnf():
    return jsonify(VIcsnf().delete(request.form))

@app.route('/createfaces', methods=["PUT"])
def create_nfd_face():
    return jsonify(NfdFace().create(request.form))

@app.route('/deletefaces', methods=["PUT"])
def delete_nfd_face():
    return jsonify(NfdFace().delete(request.form))

@app.route('/nfd-route', methods=["POST"])
def create_nfd_route():
    return jsonify(NfdRoute().create(request.form))

if __name__ == '__main__':
    app.run()
