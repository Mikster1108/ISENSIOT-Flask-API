import os
from flask import Blueprint, send_file, request, jsonify, url_for
from security import SCFlask
from video.fetch_video import fetch_all_video_paths, fetch_video_path_by_filename

from video.filter import sort_videos

api = Blueprint('video', __name__)
requires_authentication = SCFlask.requires_authentication

VIDEOS_PER_PAGE = 8
temp_zip_file = os.path.join("Temporary-zip-storage", "data.zip")
zip_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), temp_zip_file)


@api.route('/all', methods=['GET'])
@requires_authentication
def get_all_video_filenames():
    page = request.args.get('page', default=1, type=int)
    query_filter = request.args.get('filter')

    video_paths = fetch_all_video_paths()
    sorted_videos = sort_videos(video_paths=video_paths, query_filter=query_filter)
    total_items = len(sorted_videos)

    start_index = (page - 1) * VIDEOS_PER_PAGE
    end_index = start_index + VIDEOS_PER_PAGE
    items = [os.path.basename(filename) for filename in sorted_videos[start_index:end_index]]

    next_page = page + 1 if end_index < total_items else None
    prev_page = page - 1 if start_index > 0 else None

    next_link = url_for('video.get_all_video_filenames', page=next_page, _external=True) if next_page else None
    prev_link = url_for('video.get_all_video_filenames', page=prev_page, _external=True) if prev_page else None

    response_data = {
        'items_per_page': len(items),
        'total_items': total_items,
        'page': page,
        'next': next_link,
        'previous': prev_link,
        'items': items
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
