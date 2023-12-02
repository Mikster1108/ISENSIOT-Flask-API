from flask import abort
from app_setup import User
import http.client


def fetch_all_users():
    users = User.query.all()
    return users


def fetch_user(user_email):
    user = User.query.filter_by(email=user_email).first()

    if not user:
        abort(http.client.BAD_REQUEST, "User not found")
    return user


