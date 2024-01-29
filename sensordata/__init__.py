from flask import Blueprint
from security import SCFlask

api = Blueprint('sensor_data', __name__)
requires_authentication = SCFlask.requires_authentication
