# VigilantVision Deployment

## Features
- Live camera feed streaming via MJPEG endpoint.
- Threat classification (weapon vs person).
- SQLite logging of detections.
- Docker and Docker Compose setup for quick deployment.

## Run Locally
```bash
# Backend
cd backend
pip install -r ../requirements.txt
python app.py

# Frontend
open ../frontend/index.html
```

## Docker
```bash
docker-compose build
docker-compose up
```


```markdown
# VigilantVision Deployment

## Project Introduction
VigilantVision is a full‑stack, AI‑powered surveillance solution that detects faces and classifies threats (e.g. weapons vs. people) in real time. It provides:

- **Live camera streaming** with annotated bounding boxes  
- **Threat classification** using YOLOv5 to distinguish weapons from innocuous objects  
- **Face detection** via OpenCV Haar cascades  
- **Detection logging** into a lightweight SQLite database  
- **Web frontend** to view live MJPEG stream  
- **Deployment** via Docker & Docker Compose for “one‑command” launch  

---

## Architecture Overview

```

┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│ USB Camera  │ ───▶ │  Flask App   │ ───▶ │  Frontend     │
│ (/dev/video0)│     │  (`/stream`) │      │  (index.html) │
└─────────────┘      └──────────────┘      └───────────────┘
│
▼
┌──────────────┐
│  Detector    │
│  Module      │
└──────────────┘
│
┌──────────┴───────────┐
│                      │
▼                      ▼
Face Detection         Threat Detection
(Haarcascade)           (YOLOv5)
│                      │
└──────────┬───────────┘
▼
┌──────────────┐
│   Database   │
│  (SQLite)    │
└──────────────┘

```

---

## Models & Modules Used

### 1. Face Detection
- **Model:** `haarcascade_frontalface_default.xml` (OpenCV Haar Cascade)  
- **Library:** `opencv-python-headless`

### 2. Threat Detection
- **Model:** `yolov5s` pretrained on COCO (Ultralytics Yolov5)  
- **Library:** `torch`, `ultralytics`

### 3. Web Framework & API
- **Flask** — lightweight Python web framework  
- **Flask‑CORS** — enable cross‑origin requests for the frontend  
- **Gunicorn** — production WSGI server  

### 4. Database
- **SQLite** — file‑based SQL database, accessed via Python’s built‑in `sqlite3`

### 5. Frontend
- **HTML5** + **Vanilla JavaScript** — displays live MJPEG stream  

### 6. Deployment
- **Docker** — containerizes the app  
- **docker‑compose** — orchestrates service, camera device mapping, and volume mounts

---

## Directory & File Structure

```

VigilantVision\_Deployment/
├── backend/
│   ├── app.py           # Flask app: /stream & /detect endpoints
│   ├── detector.py      # process\_frame() integrating Haar & YOLO
│   └── db.py            # init\_db(), insert\_log()
├── frontend/
│   └── index.html       # Live stream viewer
├── models/
│   └── haarcascade\_frontalface\_default.xml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md            # (this file)

````

---

## Setup & Installation

1. **Clone or unzip** the project root.  
2. **Add models**:
   - Place `haarcascade_frontalface_default.xml` under `models/`.
   - (Optional) Add custom YOLO `.pt` weights in `models/` and update `detector.py` load path.

3. **Install dependencies** (local testing):
   ```bash
   cd backend
   pip install --no-cache-dir -r ../requirements.txt
````

---

## Local Usage

1. **Start backend**:

   ```bash
   cd backend
   python app.py
   ```
2. **View stream**:

   * Open `frontend/index.html` in your browser.
   * Live annotated video appears via MJPEG at `http://localhost:5000/stream`.

---

## Docker Deployment

1. **Build & launch**:

   ```bash
   docker-compose build
   docker-compose up
   ```
2. **Access**:

   * Visit `http://localhost:5000/stream` to see live feed.
   * Containers map your host’s `/dev/video0`, so ensure your camera is accessible.

---

## Next Steps & Customization

* **HTTPS / SSL**: Add an Nginx reverse proxy for TLS termination.
* **Custom YOLO Models**: Replace `yolov5s` with your fine‑tuned model by updating `detector.py`.
* **UI Enhancements**: Add controls to capture snapshots, view logs dashboard, or configure detection thresholds.
* **Scaling**: Swap SQLite for PostgreSQL and run multiple Gunicorn workers behind a load balancer.

---

Thank you for choosing VigilantVision—your AI‑driven guardian for real‑time surveillance!


🏁 Quick Start
1. Add Models
Place your haarcascade_frontalface_default.xml into the models/ folder alongside any custom YOLO weights if needed.

✅ Features Included:
Backend (Flask API): Accepts image input, performs face & threat detection, logs results in a SQLite database.

Frontend (HTML/JS): Lets you upload images and view the detection results.

Database (SQLite): Automatically created and updated with detection logs.

Pre-integrated Models:

YOLOv5 via Ultralytics (auto-downloaded)

You must add haarcascade_frontalface_default.xml into the models/ folder.

🧠 AI Models
Face Detection: OpenCV Haarcascade.

Threat Detection: YOLOv5s (weapons, persons, etc.).