import cv2

import numpy as np


class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath, filterPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        self.filterPath = filterPath

        #########

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()
        self.readFilterList()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')

    def readFilterList(self):
        with open(self.filterPath, 'r') as p:
            self.filterList = p.read().splitlines()

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)
        itemsFoundList = []
        activationItem = None

        if (cap.isOpened() == False):
            print("Error opening file...")
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
                            itemsFoundList.insert(-1, str(classLabel))
                        if activationItem is None:
                            activationItem = classLabel

            (succes, image) = cap.read()

        cv2.destroyAllWindows()
        return itemsFoundList, activationItem
