# Gesture-controlled-servo
Gesture controlled servo with real-time hand tracking 
This project implements a real-time gesture-controlled servo system using computer vision and microcontroller integration. A webcam captures live video input, a hand landmark detection model identifies key finger positions, and the distance between the thumb and pinky is used to control the rotation of a servo motor.
The system transforms human hand motion into mechanical movement through a full perception-to-actuation pipeline.


How It Works
Video Capture (OpenCV)
Captures live frames from the webcam.
Mirrors the image for natural interaction.
Hand Landmark Detection (MediaPipe)
Uses a pre-trained hand tracking model.
Detects 21 hand landmarks in real time.
Geometric Processing
Extracts landmark 4 (thumb tip) and landmark 20 (pinky tip).
Computes Euclidean distance between them.
Distance-to-Angle Mapping
Converts pixel distance into a 0–180° servo range.

Hardware Communication
Sends angle values via PyFirmata to an Arduino.
Arduino generates PWM signal to control the servo motor.

Tech Stack
Python
OpenCV
MediaPipe Tasks API
NumPy
PyFirmata
Arduino Uno
SG90 Servo Motor

Challenges Faced
Finding compatible versions of the software used(mediapipe only working with python 3.9)
Calibrating distance ranges for accurate servo mapping.
Reducing jitter caused by small landmark fluctuations.
Designing a visually clean way to show the detection of finger motion

Setup Instructions
Install Python 3.9
Install dependencies:
  pip install -r requirements.txt
Upload StandardFirmata to Arduino.
Update COM port in the script.
Run:
python servo.py
