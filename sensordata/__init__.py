from flask import Blueprint, jsonify

api = Blueprint('sensor_data', __name__)


@api.route("/", methods=['GET', 'POST'])
def some_data():
    data = [{'timestamp': 'now', 'value': 69}]
    return jsonify(data)
