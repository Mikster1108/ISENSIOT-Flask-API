import base64
import os
import cv2
from app_setup import socketio


STREAM_PORT = 8089
STREAM_URL = f"http://{os.getenv('RASPBERRY_PI_IP')}:{STREAM_PORT}/0/stream" if os.getenv('RASPBERRY_PI_IP') else 0


class CameraThread:
    def __init__(self):
        self.streaming = False
        self.main_thread = None

    def start(self):
        self.streaming = True
        self.main_thread = socketio.start_background_task(target=self.run)  # Stream starting process is not ran in bg

    def stop(self):
        self.streaming = False
        if self.main_thread:
            self.main_thread.join()
            self.main_thread = None

    def run(self):
        cap = cv2.VideoCapture(STREAM_URL)
        while self.streaming:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('frame', {'data': frame_data})
            socketio.sleep(1 / 60)
        cap.release()
