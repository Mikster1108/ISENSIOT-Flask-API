import re
from video.exceptions import InvalidFilenameException


def validate_filename(filename):
    pattern = re.compile(r'\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2}\.mp4')

    if not pattern.match(filename):
        raise InvalidFilenameException
