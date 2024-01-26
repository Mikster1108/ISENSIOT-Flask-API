from flask import Blueprint, request
from livestream.handle_camera_feed import CameraThread
from livestream.record_stream import connect_ssh
from livestream.socket_listeners import addListener, removeListener, getListenersAmount
from security import SCFlask
from app_setup import socketio
from flask_socketio import emit

api = Blueprint('livestream', __name__)
requires_authentication = SCFlask.requires_authentication
camera_thread = CameraThread()
RECORDING_TIME_SECONDS = 90


@socketio.on('connect')
@requires_authentication
def handle_connect():
    addListener(request.sid)
    emit('connect_response', {'data': 'Client connected!'})


@socketio.on('disconnect')
def handle_disconnect():
    removeListener(request.sid)
    if getListenersAmount() == 0:
        camera_thread.stop()
    emit('disconnect_response', {'data': 'Client disconnected!'})


@socketio.on('start-stream')
def handle_stream_request():
    if not camera_thread.main_thread:
        emit('start_stream_response', {'data': 'Starting stream'})
        camera_thread.start()
    else:
        emit('start_stream_response', {'data': 'Stream is already running'})


@socketio.on('start-recording')
def start_recording():
    recording = connect_ssh()
    # recording = True
    if recording:
        emit('start_recording_response', {'data': 'Camera is recording...'})

        socketio.start_background_task(target=emit_recording_message)
    elif recording is False:
        emit('start_recording_response', {'error': 'Failed to start recording'})


def emit_recording_message():
    for _ in range(5):
        socketio.sleep(1)
        socketio.emit('start_recording_response', {'data': 'Camera is recording...'})
    socketio.sleep(2)
    socketio.emit('start_recording_response', {'data': 'Camera is done recording'})
