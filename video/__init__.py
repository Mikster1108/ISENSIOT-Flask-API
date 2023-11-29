from flask import Blueprint

video = Blueprint('video', __name__)


@video.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
