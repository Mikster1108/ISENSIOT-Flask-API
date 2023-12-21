from flask import Blueprint
from security import SCFlask
from app_setup import socketio
from flask_socketio import emit

api = Blueprint('live-stream', __name__)
requires_authentication = SCFlask.requires_authentication


@socketio.on('connect', namespace='/test')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/test')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message', namespace='/test')
def handle_message(message):
    print('Received message:', message)
    emit('response', {'data': 'Message received'}, namespace='/test')
