import http.client
import os
from flask import Blueprint, jsonify, request, abort
from flask_login import  login_user
from app_setup import user_datastore, db, security
from security import SCFlask
from user.fetch_users import fetch_all_users, fetch_user
from werkzeug.security import generate_password_hash, check_password_hash
from user.user_roles import Rolename, all_roles


api = Blueprint('user', __name__)
requires_authentication = SCFlask.requires_authentication


@api.route("/index", methods=['GET'])
@requires_authentication
def index():
    users = fetch_all_users()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@api.route("/register", methods=['POST'])
def register():
    code = request.json.get('access_code')
    if not code:
        abort(http.client.BAD_REQUEST, "Access code is missing")
    else:
        if code != os.getenv('ACCESS_CODE'):
            abort(http.client.BAD_REQUEST, "Access code is incorrect")

    try:
        user_datastore.create_user(
            email=request.json.get('email'),
            password=generate_password_hash(request.json.get('password')),
            roles=[Rolename.USER.value]
        )
        db.session.commit()
    except Exception as e:
        abort(http.client.BAD_REQUEST, "Something went wrong with storing user to database, check mail and password")

    return jsonify("Created user"), 201


@api.route("/login", methods=['POST'])
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


