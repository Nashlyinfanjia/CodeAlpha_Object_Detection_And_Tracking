# 🚀 CodeAlpha_SecuritySurveillance
### Advanced Autonomous Security Surveillance System

An AI-powered real-time surveillance system built with **YOLOv8**, **ByteTrack**, and **OpenCV** that detects intrusions, scores threats dynamically, and captures forensic evidence — entirely without human intervention.

---

## 📁 Project Structure

```
CodeAlpha_SecuritySurveillance/
│
├── main.py               # Core surveillance loop
├── config.py             # All tunable settings (zones, thresholds, hours)
├── tracker.py            # ByteTrack integration
├── detector.py           # YOLOv8 detection pipeline
├── utils/
│   ├── geometry.py       # Polygon zone math & drawing
│   └── alert_system.py   # Threat scoring, HUD, evidence capture
│
├── evidence/             # Auto-saved intrusion screenshots
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the system
python main.py
```

> YOLOv8 will auto-download `yolov8n.pt` on first run.

---

## 🔧 Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `VIDEO_SOURCE` | `0` | Webcam index or path to video file |
| `YOLO_MODEL_PATH` | `yolov8n.pt` | Model weights (n/s/m/l/x) |
| `DETECTION_CONF` | `0.40` | Minimum detection confidence |
| `RESTRICTED_ZONE` | Centre box | NumPy polygon vertex array |
| `AFTER_HOURS_START` | `20` (8 PM) | Monitoring start hour (24 h) |
| `AFTER_HOURS_END` | `7` (7 AM) | Monitoring end hour (24 h) |
| `THREAT_PER_INTRUSION` | `25` | Score added per intruder per frame |
| `EVIDENCE_MIN_INTERVAL_S` | `5` | Cooldown between evidence saves |

### Customising the restricted zone
Edit the `RESTRICTED_ZONE` array in `config.py` with pixel coordinates matching your camera view:

```python
RESTRICTED_ZONE = np.array([
    [x1, y1],
    [x2, y2],
    [x3, y3],
    [x4, y4],
], dtype=np.int32)
```

---

## 🔑 Key Features

- **Real-time person detection** – YOLOv8n runs fast enough for live feeds
- **Persistent track IDs** – ByteTrack maintains identity across frames
- **Polygon geofencing** – Flexible zone shape; foot-point used for accuracy
- **Dynamic threat scoring** – Score rises with each intruder frame, decays when clear
- **Three threat levels** – LOW / MEDIUM / HIGH with colour-coded HUD
- **Flashing alert banner** – Visible intrusion notification on screen
- **Automatic evidence capture** – Timestamped JPEGs saved to `evidence/`
- **After-hours simulation** – Configurable operational window

---

## 🎯 Applications

- Office & corporate security
- Server room protection
- Warehouse & logistics monitoring
- Restricted-area surveillance
- Smart building systems

---

## 🛠 Technologies

| Library | Purpose |
|---|---|
| `ultralytics` (YOLOv8) | Object detection + ByteTrack |
| `opencv-python` | Video I/O, drawing, image saving |
| `numpy` | Array math, polygon operations |

---

## 📸 Evidence Files

Captured images are stored in `evidence/` with the naming convention:

```
breach_YYYYMMDD_HHMMSS_ids<ID_LIST>_threat<SCORE>.jpg
```

---

*Developed as part of the CodeAlpha AI Internship Program.*
