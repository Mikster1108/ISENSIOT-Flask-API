import os.path
from datetime import datetime
import cv2


def filename_to_datetime(filename):
    format_str = "%d-%m-%Y-%H-%M-%S.mp4"
    return datetime.strptime(filename, format_str)


def get_video_duration(file_path):
    try:
        video = cv2.VideoCapture(file_path)

        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = video.get(cv2.CAP_PROP_FPS)

        duration = frame_count / frame_rate

        return duration
    except Exception as e:
        return 0
    finally:
        video.release()


def sort_videos(video_paths, query_filter=None):
    if query_filter == 'date':
        # Newest video is the first one in the list
        sorted_video_paths = sorted(video_paths, key=lambda filepath: filename_to_datetime(os.path.basename(filepath)), reverse=True)
    elif query_filter == 'duration':
        # Shortest video is the first one in the list
        sorted_video_paths = sorted(video_paths, key=lambda filepath: get_video_duration(filepath))
    else:
        sorted_video_paths = video_paths

    return sorted_video_paths
