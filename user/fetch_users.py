from flask import abort, jsonify
from app_setup import db, user_datastore, User
import http.client


def fetch_all_users():
    users = User.query.all()
    return users


def fetch_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        abort(http.client.BAD_REQUEST, "User not found")
    return user


def fetch_admin_users():
    all_users = User.query.all()
    admin_users = []
    for u in all_users:
        if "admin" in u.roles:
            admin_users.append(u)

    return admin_users

