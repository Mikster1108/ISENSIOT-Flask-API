import cv2

import numpy as np


class Detector:
    def __init__(self, video_path, config_path, model_path, classes_path, filter_path):
        self.classesList = None
        self.filterList = None
        self.videoPath = video_path
        self.configPath = config_path
        self.modelPath = model_path
        self.classesPath = classes_path
        self.filterPath = filter_path

        # input settings for the detection model
        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.read_classes()
        self.read_filter_list()

    def read_classes(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')

    def read_filter_list(self):
        with open(self.filterPath, 'r') as p:
            self.filterList = p.read().splitlines()

    def analyze_recording(self):
        cap = cv2.VideoCapture(self.videoPath)
        itemsFoundList = []
        timestamps = []

        if not cap.isOpened():
            return

        (succes, image) = cap.read()

        while succes:
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold=0.6)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

            if len(bboxIdx) != 0:
                for i in range(0, len(bboxIdx)):
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]

                    if classLabel in self.filterList:
                        if classLabel not in itemsFoundList:
                            itemsFoundList.append(str(classLabel))
                            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))

            (succes, image) = cap.read()

        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration_sec = round(frames / fps)
        return itemsFoundList, timestamps, duration_sec
