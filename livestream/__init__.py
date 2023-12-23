from flask import Blueprint
from livestream.handle_camera_feed import check_if_thread_is_running, start_camera_thread, stop_camera_thread
from security import SCFlask
from app_setup import socketio
from flask_socketio import emit

api = Blueprint('livestream', __name__)
requires_authentication = SCFlask.requires_authentication


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
    if not check_if_thread_is_running('camera_thread'):
        socketio.start_background_task(target=start_camera_thread())
    else:
        emit('response', {'data': 'Stream is already running'})


@socketio.on('stop-stream')
def handle_stop_stream_request():
    if check_if_thread_is_running('camera_thread'):
        stop_camera_thread()
    else:
        emit('stop_stream_response', {'data': 'No running stream at the moment'})
