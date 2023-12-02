from flask import Blueprint, jsonify
from security import SCFlask

api = Blueprint('sensor_data', __name__)
requires_authentication = SCFlask.requires_authentication


@api.route("/", methods=['GET'])
@requires_authentication
def some_data():
    data = [{'timestamp': 'now', 'value': 69}]
    return jsonify(data), 200
