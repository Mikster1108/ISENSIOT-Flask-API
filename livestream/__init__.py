from flask import Blueprint
from livestream.handle_camera_feed import CameraThread
from security import SCFlask
from app_setup import socketio
from flask_socketio import emit

api = Blueprint('livestream', __name__)
requires_authentication = SCFlask.requires_authentication

camera_thread = CameraThread()


@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Client connected!'})


@socketio.on('disconnect')
def handle_disconnect():
    emit('response', {'data': 'Client disconnected!'})


@socketio.on('message')
def handle_message(message):
    emit('response', {'data': 'Message received'})


@socketio.on('start-stream')
def handle_stream_request():
    if not camera_thread.thread:
        camera_thread.start()
        emit('response', {'data': 'Stream is starting'})
    else:
        emit('response', {'data': 'Stream is already running'})


@socketio.on('stop-stream')
def handle_stop_stream_request():
    if camera_thread.thread:
        camera_thread.stop()
        emit('response', {'data': 'Stream is stopping'})
    else:
        emit('stop_stream_response', {'data': 'No running stream at the moment'})
