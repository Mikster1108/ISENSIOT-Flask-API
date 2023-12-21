from app_setup import User
from user.exceptions import UserNotFoundException


def fetch_all_users():
    users = User.query.all()
    return users


def fetch_user(user_email):
    user = User.query.filter_by(email=user_email).first()

    if not user:
        raise UserNotFoundException
    return user


