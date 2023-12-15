import os

from machine_learning.object_recognition.detector import Detector


class DetectorController:
    def analyze_video(video_path=str):
        project_root = os.path.dirname(os.path.abspath(__file__))
        data_folder = "model_data"

        configPath = os.path.join(project_root, data_folder, "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        modelPath = os.path.join(project_root, data_folder, "frozen_inference_graph.pb")
        classesPath = os.path.join(project_root, data_folder, "coco.names")
        filterPath = os.path.join(project_root, data_folder, "filter-object-list.names")

        object_detector = Detector(video_path, configPath, modelPath, classesPath, filterPath)
        itemsFoundList, activationItem = object_detector.onVideo()
        return itemsFoundList, activationItem
