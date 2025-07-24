import cv2
import torch

# Load models
face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define weapon classes in COCO
WEAPON_CLASSES = ['knife', 'cutting board', 'scissors', 'person']  # example

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # YOLO inference
    results = yolo_model(frame)
    detections = results.xyxy[0].tolist()  # x1,y1,x2,y2,conf,cls
    threats = []
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = yolo_model.names[int(cls)]
        threat_type = 'weapon' if label in WEAPON_CLASSES and label != 'person' else 'person'
        threats.append([x1, y1, x2, y2, conf, int(cls), threat_type])
    return faces, threats