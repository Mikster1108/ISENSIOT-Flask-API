import http

from flask import Blueprint, jsonify, abort

sensor_data = Blueprint('sensor_data', __name__)


@sensor_data.route("/")
def some_data():
    data = [{'timestamp': 'now', 'value': 69}]
    return jsonify(data)
