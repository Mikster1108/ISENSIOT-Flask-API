from flask import Flask
from user import user
from sensordata import sensor_data
from video import video

app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(sensor_data, url_prefix='/sensor_data')
app.register_blueprint(video, url_prefix='/video')
