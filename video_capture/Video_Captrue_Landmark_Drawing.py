from picamera2 import Picamera2, Preview
import time
import cv2

import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils




def initialize_camera():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.start()
    return picam2

def kill_camera_processes(picam2):
    picam2.stop()
    cv2.destroyAllWindows()

def capture_camera_frame(picam2):
    return picam2.capture_array()

    




picam2 = initialize_camera()

try:
    with mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        while True:
            frame = capture_camera_frame(picam2)          
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, handLandmarks, mp_hands.HAND_CONNECTIONS)
            cv2.imshow("Live camera feed", frame)        
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
finally:
            kill_camera_processes(picam2)

