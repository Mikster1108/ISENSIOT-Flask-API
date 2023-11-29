from flask import Blueprint

api = Blueprint('video', __name__)


@api.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
