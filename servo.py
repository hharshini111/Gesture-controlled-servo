#imports
import cv2
import mediapipe as mp
import math
from pyfirmata import Arduino, util
import numpy as np
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Arduino setup
LIGHT_PINK = (203, 192, 255)   # line color
DARK_PINK = (147, 20, 255)     # dot color
my_port = "COM5"  

#status updates
print("code check script")
board = Arduino(my_port)
print("code check arduino")

it = util.Iterator(board)
it.start()
servo = board.get_pin("d:10:s")  # Servo on 10

def move_servo(angle):
    servo.write(angle)

# Cam open+update
cap = cv2.VideoCapture(0)
print("Camera opened!")

# MediaPipe stuff
model_path = "hand_landmarker.task"

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

# Main loop
distance = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)

    # Convert to RGB(for mediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=image_rgb
    )
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            lmList = []
            h, w, _ = image.shape

            for id, lm in enumerate(hand_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if id in [4, 20]:
                    cv2.circle(image, (cx, cy), 10, DARK_PINK, cv2.FILLED)

            # Thumb tip = 4, Index tip = 8
            # Thumb tip = 4, Pinky tip = 20
            distance = math.hypot(
                lmList[20][1] - lmList[4][1],
                lmList[20][2] - lmList[4][2]
            )

            angle = np.interp(distance, [30, 300], [0, 180])
            print(f"Distance: {distance:.2f}, Angle: {angle:.2f}")
            move_servo(angle)

            # line between fingers
            cv2.line(
            image,
            (lmList[4][1], lmList[4][2]),
            (lmList[20][1], lmList[20][2]),
            LIGHT_PINK, 3
        )

    cv2.imshow("Gesture Servo Control", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
board.exit()