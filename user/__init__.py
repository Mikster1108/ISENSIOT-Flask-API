import http.client
import os
import sqlalchemy
from flask import Blueprint, jsonify, request, abort
from app_setup import user_datastore, db, limiter, security
from security import SCFlask
from user.exceptions import UserNotFoundException, InvalidEmailException, InvalidPasswordException
from user.fetch_users import fetch_all_users, fetch_user
from werkzeug.security import generate_password_hash, check_password_hash
from user.user_roles import Rolename, all_roles
from user.validate_parameters import validate_email, validate_password

api = Blueprint('user', __name__)
requires_authentication = SCFlask.requires_authentication


@api.route("/register", methods=['POST'])
@limiter.limit("5 per minute")
def register():
    code = request.json.get('access_code')
    email = request.json.get('email')
    password = request.json.get('password')

    if not code:
        abort(http.client.BAD_REQUEST, "Access code is missing")
    else:
        if code != os.getenv('ACCESS_CODE'):
            abort(http.client.BAD_REQUEST, "Access code is incorrect")

    try:
        validate_email(email)
        validate_password(password)

        user = user_datastore.create_user(
            email=email,
            password=generate_password_hash(password),
        )
        db.session.commit()

        token = create_token(email, password)
        return jsonify(user.serialize(token)), 201
    except InvalidEmailException:
        abort(http.client.BAD_REQUEST, "Not a valid email")
    except InvalidPasswordException:
        abort(http.client.BAD_REQUEST, "Not a valid password, password needs to be 5 characters long with one uppercase and one lowercase letter")
    except sqlalchemy.exc.IntegrityError as e:
        abort(http.client.BAD_REQUEST, "Email already in use")
    except Exception as e:
        abort(http.client.BAD_REQUEST, "Something went wrong with storing user to database")

    return jsonify({"error": "User could not be registered, try again"})


@api.route("/login", methods=['POST'])
@limiter.limit("10 per minute")
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    token = create_token(email, password)
    if token:
        return jsonify({"token": token}), 200
    else:
        abort(http.client.UNAUTHORIZED, "Invalid credentials")


# This cant be moved because of circular import issues
def create_token(email, password):
    try:
        user = fetch_user(email)
        token = None

        if check_password_hash(user.password, password):
            token = security.remember_token_serializer.dumps(user.fs_uniquifier)
        return token
    except UserNotFoundException:
        abort(http.client.NOT_FOUND, "User not found")
    except Exception:
        abort(http.client.BAD_REQUEST, "Incorrect password")