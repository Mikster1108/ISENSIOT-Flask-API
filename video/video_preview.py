import os
import cv2
from flask import send_file
from video import InvalidFilenameException, fetch_video_path_by_filename, fetch_video_preview
from video.exceptions import FileCouldNotBeOpened


def generate_video_preview(video_filename):
    video_preview_name = f"{video_filename.split('.')[0]}.png"
    try:
        try:
            video_preview_path = fetch_video_preview(video_preview_name)
            response = send_file(video_preview_path, mimetype='image/png')

            return response
        except InvalidFilenameException:
            pass
        except FileNotFoundError:
            pass
        except IsADirectoryError:
            pass

        video_path = fetch_video_path_by_filename(video_filename)
        if not os.path.exists(video_path):
            raise FileNotFoundError("Video file not found")

        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise FileCouldNotBeOpened

        preview_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), f"/Video-previews/{video_preview_name}")
        cv2.imwrite(preview_path, frame)

        response = send_file(preview_path, mimetype='image/png')

        return response
    except InvalidFilenameException:
        raise
    except FileNotFoundError:
        raise
    except IsADirectoryError:
        raise
    except FileCouldNotBeOpened:
        raise
