from functools import wraps
import http.client
from flask import request, jsonify
from flask_socketio import disconnect
from itsdangerous import BadTimeSignature, BadSignature
from app_setup import security, User, socketio


def validate_token(token):
    try:
        token_payload = security.remember_token_serializer.loads(token)
        user = User.query.filter_by(fs_uniquifier=token_payload).first()
        return bool(user)
    except BadSignature:
        raise


class SCFlask:

    @classmethod
    def requires_authentication(cls, method):
        """" Decorator to check if you're a registered user """

        @wraps(method)
        def wrapper(*args, **kwargs):
            if request.headers.get("Authorization"):
                request_token = request.headers.get("Authorization")
                request_token = request_token.split("Bearer ")[1]  # Remove "Bearer" part from authorization
            elif request.args.get('token'):
                request_token = request.args.get('token')
            else:
                # todo: check properly if user is connected
                try:
                    disconnect()
                except Exception:
                    pass
                return jsonify({'error': 'No token'}), http.client.UNAUTHORIZED

            try:
                authorized = validate_token(request_token)
            except BadTimeSignature as e:
                disconnect()
                return jsonify({'error': 'Invalid token'}), http.client.UNAUTHORIZED

            if not authorized:
                disconnect()
                return jsonify({'error': 'Not authorized'}), http.client.UNAUTHORIZED
            return method(*args, **kwargs)

        return wrapper
