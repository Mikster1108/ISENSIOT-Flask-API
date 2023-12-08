import os.path
from datetime import datetime
from moviepy.editor import VideoFileClip


def filename_to_datetime(filename):
    format_str = "%d-%m-%Y-%H-%M-%S.mp4"
    return datetime.strptime(filename, format_str)


def get_video_duration(file_path):
    try:
        video_clip = VideoFileClip(file_path)
        duration = video_clip.duration
        return duration
    except Exception as e:
        return None


def sort_videos(video_paths, query_filter=None):
    try:
        if query_filter == 'date':
            sorted_video_paths = sorted(video_paths, key=lambda filepath: filename_to_datetime(os.path.basename(filepath)), reverse=True)
        elif query_filter == 'duration':
            sorted_video_paths = sorted(video_paths, key=lambda filepath: get_video_duration(filepath))
        else:
            sorted_video_paths = video_paths
    except Exception as e:
        sorted_video_paths = video_paths

    return sorted_video_paths
