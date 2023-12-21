from flask import jsonify


def bad_request(error):
    return jsonify({"error": error.description}), 400


def unauthorized(error):
    return jsonify({"error": error.description}), 401


def not_found(error):
    return jsonify({"error": error.description}), 404


def too_many_requests(error):
    return jsonify({"error": error.description}), 429


def internal_server_error(error):
    return jsonify({"error": error.description}), 500


