import base64
import cv2

from app_setup import socketio


class CameraThread:
    def __init__(self):
        self.streaming = False
        self.main_thread = None

    def start(self):
        self.streaming = True
        self.main_thread = socketio.start_background_task(target=self.run)

    def stop(self):
        self.streaming = False
        if self.main_thread:
            self.main_thread.join()
            self.main_thread = None

    def run(self):
        print("Starting stream...")
        cap = cv2.VideoCapture(0)
        print("Loading frames...")
        while self.streaming:
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('frame', {'data': frame_data})
            socketio.sleep(1 / 30)
        print("Stopping stream...")
        cap.release()
