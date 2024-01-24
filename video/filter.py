import os.path
from datetime import datetime
import cv2

from app_setup import app

video_durations_cache = {}
ALLOWED_EXTENSIONS = ['mp4', 'mkv', 'wmv', 'webm', 'png']


def filename_to_datetime(filename):
    format_str = f"%d-%m-%Y-%H-%M-%S.{app.config['DEFAULT_VIDEO_EXTENSION']}"
    return datetime.strptime(filename, format_str)


def get_video_duration(file_path):
    if file_path in video_durations_cache:
        return video_durations_cache[file_path]

    try:
        video = cv2.VideoCapture(file_path)

        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = video.get(cv2.CAP_PROP_FPS)

        duration = frame_count / frame_rate

        video_durations_cache[file_path] = duration
        return duration
    except Exception as e:
        return None
    finally:
        video.release()


# Reverse = True gives ascending order
def sort_videos(video_paths, query_filter=None, reverse=True):
    if query_filter == 'date':
        sorted_video_paths = sorted(video_paths, key=lambda filepath: filename_to_datetime(os.path.basename(filepath)), reverse=reverse)
    elif query_filter == 'duration':
        sorted_video_paths = sorted(video_paths, key=lambda filepath: get_video_duration(filepath), reverse=reverse)
    else:
        sorted_video_paths = video_paths

    return sorted_video_paths
