import re
from user import InvalidEmailException, InvalidPasswordException


def validate_email(email):
    pattern = re.compile(r'^\S+@\S+\.\S+$')

    if not pattern.match(email):
        raise InvalidEmailException


def validate_password(password):
    pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z]).{5,}$')

    if not pattern.match(password):
        raise InvalidPasswordException
