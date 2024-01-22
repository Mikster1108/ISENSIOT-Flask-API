import os
import cv2
from video import InvalidFilenameException, fetch_video_path_by_filename, fetch_video_preview
from video.exceptions import FileCouldNotBeOpened


def generate_video_preview(video_filename):
    video_preview_name = f"{video_filename.split('.')[0]}.png"
    try:
        try:
            return fetch_video_preview(video_preview_name)
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

        preview_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), "Video-previews")
        preview_path = os.path.join(preview_path, video_preview_name)
        cv2.imwrite(preview_path, frame)

        return preview_path
    except InvalidFilenameException:
        raise
    except FileNotFoundError:
        raise
    except IsADirectoryError:
        raise
    except FileCouldNotBeOpened:
        raise
