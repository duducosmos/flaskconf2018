'''
Developed by: Eduardo S. Pereira
Based on : https://www.learnopencv.com/deep-learning-object-detection-using-yolo-v3-with-opencv-python-c/
'''
import cv2
import numpy as np


class YoloModel:

    def __init__(self, confThreshold=0.5, nmsThreshold=0.4,
                 inpWidth=320, inpHeight=320,
                 classeFile='coco.names',
                 modelConfiguration='yolov3-tiny.cfg',
                 modelWeights="yolov3-tiny.weights"):
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.inpWidth = inpWidth
        self.inpHeight = inpHeight

        self.indices = []
        self.classIds = []
        self.confidences = []
        self.boxes = []

        self.classeFile = classeFile
        self.classes = self._loadClassesNames()
        self.modelConfiguration = modelConfiguration
        self.modelWeights = modelWeights
        self._loadNet()

    def _loadClassesNames(self):
        with open(self.classeFile, 'rt') as f:
            classes = f.read().rstrip("\n").split('\n')
        return classes

    def _loadNet(self):
        self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration,
                                              self.modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def process_frame(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1/255,
                                     (self.inpWidth, self.inpHeight),
                                     [0,0,0], 1, crop=False
                                     )
        self.net.setInput(blob)
        outputs = self.net.forward(self.get_outputs_names())
        self.indices, self.classIds, self.confidences, self.boxes = self.post_process(frame,
                                                                                      outputs)

    def draw_prediction(self, frame):
        self.process_frame(frame)

        for i in self.indices:
            i = i[0]
            box = self.boxes[i]
            left = box[0]
            top = box[1]
            widht = box[2]
            height = box[3]
            self._draw_prediction(frame, self.classIds[i], self.confidences[i],
                                  left, top, left+widht,top+height)

    def _draw_prediction(self, frame, classId, confidence,
                         left, top, right, bottom):
        cv2.rectangle(frame, (left,top), (right, bottom), (255,0,255), 5)
        label = "%2.f" % confidence
        if self.classes:
            assert(classId < len(self.classes))
            label = "{0}: {1}".format(self.classes[classId], label)
        labelSize, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))



    def get_outputs_names(self):
        layersNames = self.net.getLayerNames()
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def post_process(self, frame, outputs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        for out in outputs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if(confidence > self.confThreshold):
                    center_x = int(detection[0]*frameWidth)
                    center_y = int(detection[1]* frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)

        return indices, classIds, confidences, boxes

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    yolomodel = YoloModel()

    while cv2.waitKey(1) < 0:
        hasframe, frame =  cap.read()
        if not hasframe:
            cv2.destroyAllWindows()
            cv2.waitKey(3000)
            break
        yolomodel.draw_prediction(frame)
        cv2.imshow("Yolov3", frame)

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break
