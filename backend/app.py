from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from detector import process_frame
from db import insert_log
import cv2
import threading
import time
import base64
import numpy as np

app = Flask(__name__)
CORS(app)

# Video capture setup
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        faces, threats = process_frame(frame)
        # Log counts
        insert_log(len(faces), len(threats))
        # Draw annotations
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        for *box, conf, cls, label in threats:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detect', methods=['POST'])
def detect_static():
    data = request.json
    img_data = base64.b64decode(data["image"])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    faces, threats = process_frame(frame)
    insert_log(len(faces), len(threats))
    return jsonify({
        "faces": [list(map(int, face)) for face in faces],
        "threats": [
            list(map(int, threat[:4])) + [float(threat[4]), threat[5], threat[6]]
            for threat in threats
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)