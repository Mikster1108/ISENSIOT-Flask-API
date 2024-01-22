import os
import http.client
from flask import Blueprint, send_file, request, jsonify, url_for, abort
from security import SCFlask
from video.exceptions import NotConnectedToNasException, InvalidFilenameException, FileCouldNotBeOpened
from video.fetch_video import fetch_all_video_paths, fetch_video_path_by_filename, fetch_video_preview, \
    fetch_video_duration
from video.filter import sort_videos
from video.validate_parameters import validate_filename
from video.video_preview import generate_video_preview

api = Blueprint('video', __name__)
requires_authentication = SCFlask.requires_authentication

VIDEOS_PER_PAGE = 8


@api.route('/all', methods=['GET'])
@requires_authentication
def get_all_video_filenames():
    page = request.args.get('page', default=1, type=int)
    query_filter = request.args.get('filter')

    try:
        video_paths = fetch_all_video_paths()
    except NotConnectedToNasException as e:
        abort(http.client.INTERNAL_SERVER_ERROR, e.message)
    except InvalidFilenameException as e:
        abort(http.client.BAD_REQUEST, e.message)
    except FileNotFoundError:
        abort(http.client.BAD_REQUEST, f"File not found")
    except IsADirectoryError:
        abort(http.client.BAD_REQUEST, f"Specified file was a directory")

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
    filename = request.args.get('filename', default='')

    try:
        fetch_video_path_by_filename(filename)  # Check if file exists before giving link
    except InvalidFilenameException as e:
        abort(http.client.BAD_REQUEST, e.message)
    except FileNotFoundError:
        abort(http.client.BAD_REQUEST, f"File not found")
    except IsADirectoryError:
        abort(http.client.BAD_REQUEST, f"Specified file was a directory")

    video_duration_sec = fetch_video_duration(filename)
    response_data = {
        'video_link': f"{api_url}video/download?filename={filename}",
        'duration': video_duration_sec
    }

    return jsonify(response_data), 200


@api.route('/download', methods=['GET'])
@requires_authentication
def download_video():
    filename = request.args.get('filename', default='')

    try:
        video_path = fetch_video_path_by_filename(filename)
    except InvalidFilenameException as e:
        abort(http.client.BAD_REQUEST, e.message)
    except FileNotFoundError:
        abort(http.client.BAD_REQUEST, f"File not found")
    except IsADirectoryError:
        abort(http.client.BAD_REQUEST, f"Specified file was a directory")

    response = send_file(video_path, mimetype='video/mp4')

    return response


@api.route('/video-preview')
@requires_authentication
def generate_preview():
    video_name = request.args.get('filename', default='')
    try:
        preview_path = generate_video_preview(video_name)
        response = send_file(preview_path, mimetype='image/png')

        return response
    except InvalidFilenameException as e:
        abort(http.client.BAD_REQUEST, e.message)
    except FileNotFoundError:
        abort(http.client.BAD_REQUEST, f"File not found")
    except IsADirectoryError:
        abort(http.client.BAD_REQUEST, f"Specified file was a directory")
    except FileCouldNotBeOpened as e:
        abort(http.client.INTERNAL_SERVER_ERROR, e.message)
