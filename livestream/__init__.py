import http.client

from flask import Blueprint, request, jsonify
from itsdangerous import BadTimeSignature, BadSignature

from livestream.handle_camera_feed import CameraThread
from livestream.socket_listeners import addListener, removeListener, getListenersAmount
from security import validate_token, SCFlask
from app_setup import socketio
from flask_socketio import emit, disconnect

api = Blueprint('livestream', __name__)
requires_authentication = SCFlask.requires_authentication
camera_thread = CameraThread()


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
        emit('start_stream_response', {'data': 'Stream is starting'})
        camera_thread.start()
    else:
        emit('start_stream_response', {'data': 'Stream is already running'})

