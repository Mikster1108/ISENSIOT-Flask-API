from flask import Blueprint
from security import SCFlask


api = Blueprint('video', __name__)
requires_authentication = SCFlask.requires_authentication

