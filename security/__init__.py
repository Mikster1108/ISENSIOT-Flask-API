from functools import wraps
import http.client
from flask import abort, request
from itsdangerous import BadTimeSignature
from app_setup import security, User


class SCFlask:

    @classmethod
    def requires_authentication(cls, method):
        """" Decorator to check if you're a registered user """

        @wraps(method)
        def wrapper(*args, **kwargs):
            request_token = request.headers.get("Authorization")
            if not request_token:
                abort(http.client.UNAUTHORIZED, "No token")

            request_token = request_token.split("Bearer ")[1]  # Remove "Bearer" part from authorization
            authorized = False

            try:
                token_payload = security.remember_token_serializer.loads(request_token)
                user = User.query.filter_by(fs_uniquifier=token_payload).first()
                if user:
                    authorized = True
            except BadTimeSignature as e:
                abort(http.client.BAD_REQUEST, "Invalid token")

            if not authorized:
                abort(http.client.UNAUTHORIZED, "Not authorized")
            return method(*args, **kwargs)

        return wrapper
