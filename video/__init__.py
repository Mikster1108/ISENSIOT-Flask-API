import os
from flask import Blueprint, send_file, request, jsonify
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
    api_url = request.url_root
    items = len(fetch_all_video_paths())

    response_data = {
        'items': items,
        'zip_link': f"{api_url}video/download-zip"
    }

    return jsonify(response_data), 200


@api.route('/', methods=['GET'])
@requires_authentication
def get_video():
    api_url = request.url_root
    filename = request.args.get('filename')

    response_data = {
        'video_link': f"{api_url}video/download?filename={filename}"
    }

    return jsonify(response_data), 200


@api.route('/download', methods=['GET'])
@requires_authentication
def download_video():
    filename = request.args.get('filename')
    video_path = fetch_video_path_by_filename(filename)

    response = send_file(video_path, mimetype='video/mp4')

    return response


@api.route('/download-zip', methods=['GET'])
@requires_authentication
def download_zip():
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
