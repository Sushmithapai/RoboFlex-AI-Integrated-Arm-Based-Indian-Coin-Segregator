"""
coin_cam_detect.py
------------------
Run YOLOv8 coin detection live using your webcam.
Automatically shows bounding boxes and counts coins in each frame.
"""

from ultralytics import YOLO
import cv2

# Load your YOLOv8 model
model = YOLO("best.pt")   # <-- make sure best.pt is in the same folder

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("❌ Cannot open webcam")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on current frame
    results = model.predict(source=frame, conf=0.25, device='cpu', verbose=False)

    # Draw detections
    annotated_frame = results[0].plot()  # draws boxes and labels automatically


    # Show frame
    cv2.imshow("Coin Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\n✅ Camera detection stopped.")
