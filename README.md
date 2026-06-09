# CodeAlpha_Object_Detection_And_Tracking
Developed a real-time Object Detection and Tracking system using Python, OpenCV, and YOLOv8 for CodeAlpha's AI Internship . The application processes live video streams to track objects with persistent IDs and utilizes a custom-coded virtual crossing line to dynamically count objects for traffic or foot-traffic analytics.
🚀 Project Title: Real-Time Object Detection, Tracking, and Analytics Pipeline
📝 Project Overview
This project is an advanced computer vision application developed as part of the CodeAlpha Artificial Intelligence Internship (Task 4), referenced in 14300.jpg.

The core objective is to build an intelligent, real-time video processing pipeline that not only detects everyday objects but also consistently tracks them across video frames using unique IDs. To elevate this beyond a basic tutorial project, a customized "Zone of Interest" (Virtual Counting Line) and an interactive metrics dashboard were engineered into the system. This transforms the script into a practical, real-world solution suitable for traffic monitoring, retail foot-traffic analytics, or security surveillance.

✨ Key Features
Real-Time Object Detection: Integrates the state-of-the-art YOLOv8 (You Only Look Once) deep learning model to instantly identify up to 80 different classes of objects (such as people, vehicles, and electronics) via a live webcam or video file.

Persistent Object Tracking: Employs advanced, frame-to-frame tracking (ByteTrack logic) that assigns a unique, persistent ID to every detected object, ensuring they are recognized continuously even through brief occlusions.

Intelligent Line-Crossing Analytics: Features a custom-coded virtual crossing line. When an object's calculated spatial center moves past this threshold, it triggers an event that increments a global counter.

Dynamic HUD & Overlay: Uses OpenCV to render a polished, production-ready Head-Up Display (HUD). This includes color-coded bounding boxes mapped to tracking IDs, center-point markers, and a live counter dashboard overlay.

🛠️ Tech Stack & Architecture
Programming Language: Python 3

Computer Vision Framework: OpenCV (for video I/O, image processing, and dynamic UI rendering)

Deep Learning Engine: Ultralytics YOLOv8 (Nano architecture optimized for high-FPS, real-time CPU/GPU execution)

Tracking Algorithm: ByteTrack (integrated via Ultralytics API for low-latency ID persistence)

📈 Real-World Applications
The architecture used in this project mirrors commercial software used in:

Smart Cities: Counting and analyzing highway traffic flow.

Retail Analytics: Monitoring how many customers enter a specific aisle or cross a store threshold.

Automation & Security: Flagging unauthorized entry across restricted boundaries.
