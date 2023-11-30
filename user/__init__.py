import http.client
import os

from flask import Blueprint, jsonify, request, abort
from app_setup import user_datastore, db
from user.fetch_users import fetch_all_users
from werkzeug.security import generate_password_hash
from user.user_roles import Rolename, all_roles

api = Blueprint('user', __name__)


@api.route("/index", methods=['GET'])
def index():
    users = fetch_all_users()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@api.route("/register", methods=['POST'])
def register():
    code = request.form.get('access_code')
    if code is None or not code:
        abort(http.client.BAD_REQUEST, "Access code is missing")
    else:
        if code != os.getenv('ACCESS_CODE'):
            abort(http.client.BAD_REQUEST, "Access code is incorrect")

    try:
        user_datastore.create_user(
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password')),
            roles=[Rolename.USER.value]
        )
        db.session.commit()
    except Exception as e:
        print(e)
        abort(http.client.BAD_REQUEST, "Something went wrong, most likely a invalid mail or password")

    return jsonify("Created user"), 201


@api.route("/login", methods=['POST'])
def login():
    # todo: implement this xD
    pass

