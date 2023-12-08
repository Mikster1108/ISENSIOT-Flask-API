import os
from flask import Blueprint, send_file, request, jsonify, url_for
from security import SCFlask
from video.fetch_video import fetch_all_video_paths, fetch_video_path_by_filename
from zipfile import ZipFile

from video.filter import sort_videos

api = Blueprint('video', __name__)
requires_authentication = SCFlask.requires_authentication

VIDEOS_PER_PAGE = 8
temp_zip_file = os.path.join("Temporary-zip-storage", "data.zip")
zip_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), temp_zip_file)


@api.route('/all', methods=['GET'])
@requires_authentication
def get_all_videos():
    page = request.args.get('page', default=1, type=int)
    query_filter = request.args.get('filter')

    video_paths = fetch_all_video_paths()
    total_items = len(video_paths)

    start_index = (page - 1) * VIDEOS_PER_PAGE
    end_index = start_index + VIDEOS_PER_PAGE
    items = len(video_paths[start_index:end_index])

    next_page = page + 1 if end_index < total_items else None
    prev_page = page - 1 if start_index > 0 else None

    next_link = url_for('video.get_all_videos', page=next_page, _external=True) if next_page else None
    prev_link = url_for('video.get_all_videos', page=prev_page, _external=True) if prev_page else None

    api_url = request.url_root

    response_data = {
        'items': items,
        'total_items': total_items,
        'page': page,
        'next': next_link,
        'previous': prev_link,
        'zip_link': f"{api_url}video/download-zip?filter={query_filter}&page={page}"
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
    query_filter = request.args.get('filter')
    page = request.args.get('page', default=1)

    video_paths = fetch_all_video_paths()

    start_index = (page - 1) * VIDEOS_PER_PAGE
    end_index = start_index + VIDEOS_PER_PAGE

    video_paths = sort_videos(video_paths=video_paths, query_filter=query_filter)[start_index, end_index]

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
