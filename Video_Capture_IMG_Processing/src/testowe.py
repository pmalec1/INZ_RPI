from picamera2 import Picamera2, Preview
import time
import cv2
import os
import mediapipe as mp
from utils import camera_utils, detection_utils, draw_landmarks_utils, UI_utils, landmarks_processing

#Incializacja modułów mediapipe hands
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3, min_tracking_confidence=0.3,model_complexity=0)
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

#Uruchomienie kamery
picam2 = camera_utils.initialize()
camera_window_name="Live view"
camera_utils.start(picam2,camera_window_name)
x_left = int(0.2 * 640)
x_right = int(0.8 * 640)
        

try:
    while cv2.getWindowProperty(camera_window_name, cv2.WND_PROP_VISIBLE) >=1:
        
        frame = camera_utils.capture_frame(picam2)
        time1 = time.time()
        processing_results = mp_hands.process(frame)
        if detection_utils.check_if_hand_is_detected(processing_results):
          for hand_landmarks in processing_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp.solutions.hands.HAND_CONNECTIONS)
        time2 = time.time()
        fps = 1/(time2-time1)
        time1 = time2
        # Rysowanie pionowych kresek
        color = (0, 255, 0)  # Zielony
        thickness = 2
        cv2.line(frame, (x_left, 50), (x_left, 400), color, thickness)
        cv2.line(frame, (x_right, 50), (x_right, 400
                                        
                                        ), color, thickness)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        camera_utils.display_frame("Live view", frame)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
except  cv2.error as e:
    print(f"Błąd związany z oknem lub innymi operacjami OpenCV \n\n{e}")
        
finally:
    camera_utils.release_resources(picam2)
    
