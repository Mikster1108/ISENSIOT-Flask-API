from flask import Blueprint

api = Blueprint('user', __name__)


@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
