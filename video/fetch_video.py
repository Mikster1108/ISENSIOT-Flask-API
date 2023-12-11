import os
import http.client
from flask import abort

from common.fetch_file import get_file_path, get_all_file_paths
from video.validate_parameters import validate_filename

video_directory_name = "Video-recordings"
video_footage_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), video_directory_name)


def fetch_all_video_paths():
    try:
        files = [fetch_video_path_by_filename(filename) for filename in get_all_file_paths(video_footage_path)]

        return files
    except FileNotFoundError:
        abort(http.client.OK, f"No recordings available")


def fetch_video_path_by_filename(filename):
    try:
        validate_filename(filename)

        file_path = get_file_path(filename, video_footage_path)

        return file_path
    except FileNotFoundError:
        abort(http.client.BAD_REQUEST, f"File {filename} not found")
    except IsADirectoryError:
        abort(http.client.BAD_REQUEST, f"{filename} is a directory")


