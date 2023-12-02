import http.client
import os
from flask import Blueprint, jsonify, request, abort
from flask_login import login_user
from app_setup import user_datastore, db, security, limiter
from security import SCFlask
from user.fetch_users import fetch_all_users, fetch_user
from werkzeug.security import generate_password_hash, check_password_hash
from user.user_roles import Rolename, all_roles


api = Blueprint('user', __name__)
requires_authentication = SCFlask.requires_authentication


@api.route("/register", methods=['POST'])
@limiter.limit("5 per minute")
def register():
    code = request.json.get('access_code')
    if not code:
        abort(http.client.BAD_REQUEST, "Access code is missing")
    else:
        if code != os.getenv('ACCESS_CODE'):
            abort(http.client.BAD_REQUEST, "Access code is incorrect")

    try:
        user = user_datastore.create_user(
            email=request.json.get('email'),
            password=generate_password_hash(request.json.get('password')),
        )
        db.session.commit()
    except Exception as e:
        abort(http.client.BAD_REQUEST, "Something went wrong with storing user to database, check mail and password")

    return jsonify(user.serialize()), 201


@api.route("/login", methods=['POST'])
@limiter.limit("5 per minute")
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = fetch_user(email)
    if not user:
        abort(http.client.NOT_FOUND, "User not found")

    if check_password_hash(user.password, password):
        login_user(user)
        token = security.remember_token_serializer.dumps(user.fs_uniquifier)

        return jsonify({"token": token}), 200
    else:
        abort(http.client.UNAUTHORIZED, "Invalid credentials")


