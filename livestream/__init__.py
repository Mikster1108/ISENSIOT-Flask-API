from flask import Blueprint
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
