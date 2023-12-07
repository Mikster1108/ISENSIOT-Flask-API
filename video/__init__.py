import os

from app_setup import limiter
from flask import Blueprint, send_file, request
from security import SCFlask
from video.fetch_video import fetch_all_video_paths, fetch_video_path_by_filename
from zipfile import ZipFile


api = Blueprint('video', __name__)
requires_authentication = SCFlask.requires_authentication

temp_zip_file = os.path.join("Temporary-zip-storage", "data.zip")
zip_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), temp_zip_file)


@api.route('/all', methods=['GET'])
@requires_authentication
def get_all_videos():
    video_paths = fetch_all_video_paths()

    if os.path.exists(zip_path):
        os.remove(zip_path)

    with ZipFile(zip_path, 'w') as zip_file:
        for video in video_paths:
            with open(video, 'rb') as video_file:
                video_content = video_file.read()
                zip_file.writestr(os.path.basename(video), video_content)
        zip_file.close()

    response = send_file(zip_path, mimetype='application/zip', as_attachment=True)

    return response


@api.route('/', methods=['GET'])
@requires_authentication
def get_video():
    filename = request.args.get('filename')
    video_path = fetch_video_path_by_filename(filename)
    response = send_file(video_path, mimetype='video/mp4')
    return response

