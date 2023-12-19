import http.client
import re

from flask import abort


def validate_filename(filename):
    pattern = re.compile(r'\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2}\.mp4')

    if not pattern.match(filename):
        abort(http.client.BAD_REQUEST, f"File {filename} was not in the correct format")