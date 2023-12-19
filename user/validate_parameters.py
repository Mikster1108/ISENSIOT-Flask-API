import http.client
import re

from flask import abort


def validate_email(email):
    pattern = re.compile(r'^\S+@\S+\.\S+$')

    if not pattern.match(email):
        abort(http.client.BAD_REQUEST, f"Not a valid email")


def validate_password(password):
    pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z]).{5,}$')

    if not pattern.match(password):
        abort(http.client.BAD_REQUEST, f"Not a valid password, password needs to be 5 characters long with one uppercase and one lowercase letter")
