import cv2
import numpy as np
import time
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Parking slot coordinates
parking_slots = [
    (402, 239), (753, 377), (55, 100), (56, 146), (51, 241), (53, 290), (51, 192),
    (405, 189), (402, 138), (405, 90), (514, 92), (511, 139), (514, 187), (512, 236),
    (163, 99), (164, 147), (158, 194), (159, 243), (161, 290), (55, 337), (162, 339),
    (160, 388), (162, 429), (52, 431), (53, 479), (163, 479), (168, 525), (165, 576),
    (165, 620), (56, 623), (51, 573), (52, 527), (402, 289), (402, 338), (404, 382),
    (405, 427), (405, 526), (403, 569), (406, 619), (512, 524), (512, 568), (513, 620),
    (511, 426), (511, 380), (513, 329), (511, 284), (751, 88), (751, 136), (750, 188),
    (753, 232), (753, 276), (751, 327), (757, 427), (753, 472), (757, 518), (760, 573),
    (760, 616), (901, 620), (901, 576), (892, 141), (892, 190), (893, 235), (894, 284),
    (897, 330), (898, 375), (901, 424), (903, 474), (899, 522), (46, 385)
]

# Global constants
rect_width, rect_height = 100, 33
threshold = 30
last_call_time = time.time()
prevFreeslots = 0

# Convert to binary contours image
def convert_grayscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = frame.copy()
    contour_image[:] = 0
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
    return contour_image

# Draw bounding boxes and count free slots
def mark_slots(frame, grayscale_frame):
    global last_call_time, prevFreeslots
    current_time = time.time()
    freeslots = 0

    for x, y in parking_slots:
        x1, x2 = x + 10, x + rect_width - 11
        y1, y2 = y + 4, y + rect_height
        start_point, stop_point = (x1, y1), (x2, y2)

        crop = grayscale_frame[y1:y2, x1:x2]
        if crop.size == 0:
            continue
        try:
            gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        except:
            continue

        count = cv2.countNonZero(gray_crop)
        color, thick = [(0, 255, 0), 5] if count < threshold else [(0, 0, 255), 2]
        if count < threshold:
            freeslots += 1

        cv2.rectangle(frame, start_point, stop_point, color, thick)

    if current_time - last_call_time >= 0.1:
        cv2.putText(frame, "Free Slots: " + str(freeslots), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
        last_call_time = current_time
        prevFreeslots = freeslots
    else:
        cv2.putText(frame, "Free Slots: " + str(prevFreeslots), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)

    return frame

# Main function with working file dialog
def main():
    cap = None
    while cap is None:
        print("\nSelect Input Source:")
        print("1. Webcam")
        print("2. Video File")
        print("Q. Quit")
        choice = input("Enter your choice (1/2/Q): ").strip()

        if choice == '1':
            cap = cv2.VideoCapture(0)

        elif choice == '2':
            try:
                # Create file dialog and keep it on top
                root = Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                path = askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
                root.destroy()

                if path and os.path.exists(path):
                    cap = cv2.VideoCapture(path)
                else:
                    print("Invalid file or selection.")
            except Exception as e:
                print("Error opening file dialog:", e)

        elif choice.lower() == 'q':
            print("Quitting.")
            return
        else:
            print("Invalid input. Please enter 1, 2, or Q.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Video has ended or frame cannot be read.")
            break

        grayscale_frame = convert_grayscale(frame)
        out_image = mark_slots(frame, grayscale_frame)

        cv2.imshow("Parking Spot Detector", out_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User interrupted.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
