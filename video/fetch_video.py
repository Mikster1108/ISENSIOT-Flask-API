import os
from common.fetch_file import get_file_path, get_all_file_paths
from video.exceptions import InvalidFilenameException, NotConnectedToNasException
from video.validate_parameters import validate_filename

VIDEO_DIRECTORY_NAME = "Video-recordings"
VIDEO_PREVIEW_DIRECTORY_NAME = "Video-previews"

VIDEO_FOOTAGE_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), VIDEO_DIRECTORY_NAME)
VIDEO_PREVIEW_PATH = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), VIDEO_PREVIEW_DIRECTORY_NAME)


def fetch_all_video_paths():
    try:
        files = [fetch_video_path_by_filename(filename) for filename in get_all_file_paths(VIDEO_FOOTAGE_PATH)]

        return files
    except FileNotFoundError:
        raise NotConnectedToNasException


def fetch_video_path_by_filename(filename):
    try:
        if not filename:
            raise InvalidFilenameException(message="Empty filename")
        validate_filename(filename)

        file_path = get_file_path(filename=filename, target_directory=VIDEO_FOOTAGE_PATH)

        return file_path
    except FileNotFoundError:
        raise FileNotFoundError
    except IsADirectoryError:
        raise IsADirectoryError
    except InvalidFilenameException:
        raise


def fetch_video_preview(filename):
    try:
        if not filename:
            return None
        validate_filename(filename)
        file_path = get_file_path(filename=filename, target_directory=VIDEO_PREVIEW_PATH)

        return file_path
    except FileNotFoundError:
        raise FileNotFoundError
    except IsADirectoryError:
        raise IsADirectoryError
    except InvalidFilenameException:
        raise
