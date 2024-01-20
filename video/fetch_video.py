import os
from common.fetch_file import get_file_path, get_all_file_paths
from video.exceptions import InvalidFilenameException, NotConnectedToNasException
from video.validate_parameters import validate_filename

video_directory_name = "Video-recordings"
video_footage_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), video_directory_name)


def fetch_all_video_paths():
    try:
        files = [fetch_video_path_by_filename(filename) for filename in get_all_file_paths(video_footage_path)]

        return files
    except FileNotFoundError:
        raise NotConnectedToNasException


def fetch_video_path_by_filename(filename):
    try:
        if not filename:
            raise InvalidFilenameException(message="Empty filename")
        validate_filename(filename)

        file_path = get_file_path(filename, video_footage_path)

        return file_path
    except FileNotFoundError:
        raise FileNotFoundError
    except IsADirectoryError:
        raise IsADirectoryError
    except InvalidFilenameException:
        raise


