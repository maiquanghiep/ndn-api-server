from flask import Flask, request, jsonify
from service import VIcsnf

import json

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/vicsnf', methods=["POST"])
def create_vicsnf():
    return jsonify(VIcsnf().create(request.form))


if __name__ == '__main__':
    app.run()
