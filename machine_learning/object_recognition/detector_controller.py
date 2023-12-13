from detector import *
import os


class DetectorController:
    def analyze_video(video_path=str):
        configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
        classesPath = os.path.join("model_data", "coco.names")
        filterPath = os.path.join("model_data", "filter-object-list.names")

        object_detector = Detector(video_path, configPath, modelPath, classesPath, filterPath)
        itemsFoundList, activationItem = object_detector.onVideo()
        return itemsFoundList, activationItem