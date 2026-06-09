import cv2
from ultralytics import YOLO

def main():
    # 1. Load the pre-trained YOLOv8 model (nano version for real-time speed)
    model = YOLO("yolov8n.pt")

    # 2. Set up video input (0 for webcam, or replace with "your_video.mp4")
    video_path = 0 
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Define a virtual counting line (Y-coordinate on the screen)
    # Adjust this based on your camera resolution
    line_y = 300  
    crossed_ids = set()
    total_count = 0

    print("Press 'q' to exit the application.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Video stream ended or failed.")
            break

        # 3. Object Detection & Tracking via YOLO Tracker
        # persist=True keeps track of object IDs across frames
        results = model.track(frame, persist=True, device="cpu", verbose=False)

        # Draw our virtual counting line (Sophisticated Neon Cyan)
        cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 255, 0), 2)
        cv2.putText(frame, "COUNTING LINE", (10, line_y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        # 4. Process detection results
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.int().cpu().tolist()
            
            for box, id, cls in zip(boxes, ids, clss):
                # Get coordinates
                x1, y1, x2, y2 = box
                
                # Fetch class name (e.g., person, car)
                class_name = model.names[cls]
                
                # Calculate the center point of the object
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Creative Logic: Logic for Line Crossing
                if cy > line_y and id not in crossed_ids:
                    crossed_ids.add(id)
                    total_count += 1

                # 5. UI Rendering: Draw sleek bounding boxes
                # Dynamic color scheme based on tracking ID
                box_color = (int((id * 50) % 255), 255, int((id * 30) % 255))
                
                # Draw main bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                # Draw center tracking dot
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                
                # Draw a clean dark background for text label
                label = f"{class_name} ID:{id}"
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), box_color, -1)
                cv2.putText(frame, label, (x1, y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # 6. Dashboard Overlay for Metrics
        cv2.rectangle(frame, (20, 20), (220, 80), (0, 0, 0), -1)
        cv2.putText(frame, f"Total Count: {total_count}", (30, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the live window
        cv2.imshow("CodeAlpha AI - Object Tracker & Counter", frame)

        # Break loop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up and release assets
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()