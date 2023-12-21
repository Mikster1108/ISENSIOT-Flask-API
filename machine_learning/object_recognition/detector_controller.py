import os

from machine_learning.object_recognition.detector import Detector


class DetectorController:
    def __init__(self, video_directory):
        project_root = os.path.dirname(os.path.abspath(__file__))
        self.data_folder = "model_data"
        self.video_directory = video_directory
        self.filter_path = os.path.join(project_root, self.data_folder, "filter-object-list.names")
        self.config_path = os.path.join(project_root, self.data_folder, "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        self.model_path = os.path.join(project_root, self.data_folder, "frozen_inference_graph.pb")
        self.classes_path = os.path.join(project_root, self.data_folder, "coco.names")

    def analyze_recording(self, video_name):
        video_path = os.path.join(self.video_directory, video_name)
        object_detector = Detector(video_path, self.config_path, self.model_path, self.classes_path, self.filter_path)
        items_found_list, timestamps = object_detector.analyze_recording()
        return items_found_list, timestamps

    def get_new_recordings(self):
        return [f for f in os.listdir(self.video_directory) if os.path.isfile(os.path.join(self.video_directory, f))]


def run_analyzing_process(raw_footage_dir_name, analyzed_footage_dir_name):
    detector_controller = DetectorController(os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), raw_footage_dir_name))
    new_recordings_list = detector_controller.get_new_recordings()
    for recording in new_recordings_list:
        print("Starting analyzing process of " + recording)
        items_found_list, timestamps = detector_controller.analyze_recording(recording)
        print("done analyzing " + recording + " with results:")
        print(items_found_list, timestamps)
        src_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), raw_footage_dir_name, recording)
        dst_path = os.path.join(os.getenv("NAS_DRIVE_MOUNT_PATH"), analyzed_footage_dir_name, recording)
        os.rename(src_path, dst_path)

