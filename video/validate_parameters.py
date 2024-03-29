import re
from video.exceptions import InvalidFilenameException


ALLOWED_EXTENSIONS = ['mp4', 'mkv', 'wmv', 'webm', 'png']


def validate_filename(filename):
    pattern = re.compile(r'\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2}\.(\w+)$')
    match = pattern.match(filename)

    if not match:
        raise InvalidFilenameException

    extension = match.group(1).lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidFilenameException


def validate_boolean_value(value):
    return value.lower() == 'true'
