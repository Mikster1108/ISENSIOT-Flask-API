import base64
import cv2
from app_setup import socketio


streaming = False
tasks = {}


def start_camera_thread():
    global streaming
    streaming = True
    tasks['camera_thread'] = True
    print("Starting stream...")

    cap = cv2.VideoCapture(0)
    print("Loading frames...")

    while streaming:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('frame', {'data': frame_data})
        socketio.sleep(1/30)
    print("Stopping stream")
    cap.release()


def stop_camera_thread():
    global streaming
    streaming = False
    tasks.pop('camera_thread')


def check_if_thread_is_running(function_name):
    return tasks.get(function_name)
