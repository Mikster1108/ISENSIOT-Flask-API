from app_setup import app, socketio
from user import api as user
from sensordata import api as sensor_data
from video import api as video
from livestream import api as livestream

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(sensor_data, url_prefix='/sensor_data')
app.register_blueprint(video, url_prefix='/video')
app.register_blueprint(livestream, url_prefix='/livestream')

if __name__ == "__main__":
    socketio.run(app, debug=True)
