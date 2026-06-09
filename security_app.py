import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import os

def main():
    # 1. Initialization
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0) # 0 for webcam

    # Ensure evidence folder exists
    os.makedirs("evidence", exist_ok=True)

    # 2. Define Restricted Zone (Polygon Coordinates)
    # This creates a box on the right side of the screen. Adjust to fit your camera view.
    # Coordinates format: [x, y]
    zone_points = np.array([[350, 100], [620, 100], [620, 450], [350, 450]], np.int32)
    
    # Security Configuration
    is_after_hours = True # Simulated system state
    cooldown_frames = 0   # Prevents spamming evidence capture saves

    print("System Armed. Press 'q' to disengage security system.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Base system metrics per frame
        threat_score = 0
        alarm_triggered = False
        intruder_box = None

        # Run tracking pipeline
        results = model.track(frame, persist=True, device="cpu", verbose=False)

        # 3. Draw the Restricted Zone UI (Transparent Red Box)
        overlay = frame.copy()
        cv2.fillPoly(overlay, [zone_points], (0, 0, 255))
        # Blend overlay to create a semi-transparent glowing restriction zone
        cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)
        cv2.polylines(frame, [zone_points], True, (0, 0, 255), 2)
        cv2.putText(frame, "RESTRICTED SERVER ROOM", (360, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.int().cpu().tolist()
            
            for box, id, cls in zip(boxes, ids, clss):
                x1, y1, x2, y2 = box
                class_name = model.names[cls]
                
                # Calculate the bottom-center point of the object (where their feet are)
                cx = int((x1 + x2) / 2)
                cy = y2 

                # 4. Core Security Logic: Check if intruder is inside the polygon
                # cv2.pointPolygonTest checks if (cx, cy) is inside zone_points
                inside_zone = cv2.pointPolygonTest(zone_points, (cx, cy), False)

                # Visual settings for tracking boxes
                box_color = (0, 255, 0) # Green for safe/outside

                if class_name == "person":
                    if inside_zone >= 0: # Inside or on the edge of the zone
                        box_color = (0, 0, 255) # Warning Red
                        alarm_triggered = True
                        intruder_box = box
                        
                        # Calculate threat scoring dynamically
                        if is_after_hours:
                            threat_score = 99  # Critical threat
                        else:
                            threat_score = 45  # Medium threat (unauthorized zone daytime)
                    else:
                        # Person is detected but outside the restricted room
                        threat_score = max(threat_score, 10) 

                # Draw Sleek Targeted UI Box around tracked targets
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.putText(frame, f"TARGET #{id}: {class_name.upper()}", (x1, y1 - 7), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

        # 5. Handle Intrusion Alerts and Evidence Capture
        if alarm_triggered:
            # Drop a bright red alert flashing banner across the top
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 255), -1)
            cv2.putText(frame, "!!! INTRUSION DETECTED !!! BREACH IN PROGRESS", (70, 28), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Evidence Capture Logic (Runs once every 30 frames to avoid lagging/flooding storage)
            if threat_score == 99 and cooldown_frames == 0:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"evidence/INTRUDER_{timestamp}.jpg"
                
                # Save the raw current frame out to the disk as physical evidence
                cv2.imwrite(filename, frame)
                print(f"[SECURITY ALERT] Critical breach! Evidence saved to {filename}")
                cooldown_frames = 30 # Set 1-second cooldown (assuming ~30 FPS camera)

        if cooldown_frames > 0:
            cooldown_frames -= 1

        # 6. Top Left Live Metrics Operations Center Dashboard
        cv2.rectangle(frame, (15, 50), (250, 150), (30, 30, 30), -1)
        cv2.putText(frame, "SYS STATUS: ARMED", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f"AFTER HOURS: {is_after_hours}", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 1)
        
        # Color code the threat text based on critical score
        ts_color = (0, 0, 255) if threat_score >= 90 else ((0, 165, 255) if threat_score > 10 else (0, 255, 0))
        cv2.putText(frame, f"THREAT SCORE: {threat_score}", (25, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ts_color, 2)

        # Display output feed
        cv2.imshow("CodeAlpha AI - Core Security Terminal", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()