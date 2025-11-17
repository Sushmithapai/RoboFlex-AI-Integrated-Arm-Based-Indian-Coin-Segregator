import cv2
import serial
import threading
from ultralytics import YOLO
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time

# ------------------------------
# Load YOLOv8 model
# ------------------------------
model = YOLO("best.pt")     # Ensure file exists

# ------------------------------
# Serial Communication
# ------------------------------
try:
    ser = serial.Serial('COM3', 115200)
    print("Serial Connected")
except:
    ser = None
    print("⚠ No Serial Port Found")

# ------------------------------
# Tkinter UI
# ------------------------------
root = tk.Tk()
root.title("Coin Detection System")
root.geometry("900x700")

# Canvas for Video Preview
video_canvas = tk.Canvas(root, width=700, height=500, bg="black")
video_canvas.pack()

label_1rs = tk.Label(root, text="1 Rs Coins: 0", font=("Arial", 20))
label_1rs.pack()

label_2rs = tk.Label(root, text="2 Rs Coins: 0", font=("Arial", 20))
label_2rs.pack()

count_1 = 0
count_2 = 0
running = False

# ------------------------------------------------------
# Camera open → detect → stop camera → send serial → restart
# ------------------------------------------------------
def start_detection():
    global running
    running = True
    threading.Thread(target=run_camera, daemon=True).start()


def stop_detection():
    global running
    running = False


def run_camera():
    global count_1, count_2, running

    while running:
        # -------------------------------------------------
        # 1️⃣ OPEN CAMERA
        # -------------------------------------------------
        print("📷 Camera ON")
        cap = cv2.VideoCapture("http://192.0.0.4:8080/video")

        if not cap.isOpened():
            print("❌ Camera not found")
            time.sleep(1)
            continue

        detected = False

        while running and not detected:
            ret, frame = cap.read()
            if not ret:
                break

            # YOLO detection
            results = model.predict(frame, conf=0.30, verbose=False)
            annotated_frame = results[0].plot()

            # Loop through detections
            for box in results[0].boxes:
                cls = int(box.cls[0])

                if cls == 0:  # 1 Rs
                    count_1 += 1
                    label_1rs.config(text=f"1 Rs Coins: {count_1}")
                    detected = True

                    if ser:
                        ser.write(b"1")
                        print("➡ Sent Serial: 1")

                elif cls == 1:  # 2 Rs
                    count_2 += 1
                    label_2rs.config(text=f"2 Rs Coins: {count_2}")
                    detected = True

                    if ser:
                        ser.write(b"2")
                        print("➡ Sent Serial: 2")

                if detected:
                    break

            # ------------------------------
            # Display on Canvas
            # ------------------------------
            img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))

            video_canvas.image = img
            video_canvas.create_image(0, 0, anchor="nw", image=img)

        # -------------------------------------------------
        # 2️⃣ CLOSE CAMERA AFTER DETECTION
        # -------------------------------------------------
        print("📴 Camera OFF")
        cap.release()
        cv2.destroyAllWindows()

        # Wait before restarting the next loop
        time.sleep(1)

    print("🛑 Detection Stopped")


# Buttons
btn_start = tk.Button(root, text="Start Detection", font=("Arial", 16), command=start_detection)
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Stop Detection", font=("Arial", 16), command=stop_detection)
btn_stop.pack(pady=10)

root.mainloop()
