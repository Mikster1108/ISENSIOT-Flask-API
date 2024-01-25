from flask import Blueprint, request, jsonify
from livestream.handle_camera_feed import CameraThread
from livestream.record_stream import connect_ssh
from livestream.socket_listeners import addListener, removeListener, getListenersAmount
from security import SCFlask
from app_setup import socketio, limiter
from flask_socketio import emit

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
        emit('start_stream_response', {'data': 'Starting stream'})
        camera_thread.start()
    else:
        emit('start_stream_response', {'data': 'Stream is already running'})


@limiter.limit("10 per minute")
@api.route('/start-recording', methods=['GET'])
@requires_authentication
def start_recording():
    recording = connect_ssh()
    if recording:
        return jsonify({"success": "Recording..."}), 200
    elif recording is False:
        return jsonify({"error": "Failed to start recording"}), 500
    else:
        return jsonify({"status": "Waiting for camera response"}), 200
