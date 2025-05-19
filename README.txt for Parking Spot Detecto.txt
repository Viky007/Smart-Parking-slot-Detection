README.txt for Parking Spot Detector
====================================

Project Overview
----------------
This Python application analyzes a live webcam feed or a video file to detect and count free parking slots in real time. It converts each frame to a binary contour map, overlays bounding boxes for predefined slot locations, and displays the current free‐slot count.

Features
--------
- **Webcam or Video Input**: Choose between your system’s webcam or any local video file (.mp4, .avi, .mov, .mkv).  
- **Predefined Slot Coordinates**: Uses a hard-coded list of parking‐slot coordinates; easy to customize for different parking layouts.  
- **Real-time Contour Analysis**: Converts frames to binary, finds contours, and counts non-zero pixels to decide if a slot is occupied.  
- **Visual Feedback**:  
  - Green, thick rectangles for free slots  
  - Red, thin rectangles for occupied slots  
  - On-screen counter showing the number of free slots  
- **Low‐Latency Updates**: Slot count refreshes at up to 10 Hz with a brief cooldown to avoid flicker.

Requirements
------------
- Python 3.7 or higher  
- Libraries:  
  - `opencv-python`  
  - `numpy`  
  - `tkinter` (standard with most Python installs)  

Install Dependencies
--------------------
```bash
pip install opencv-python numpy
