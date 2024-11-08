from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np
import os
import mediapipe as mp
from utils import camera_utils, detection_utils, draw_landmarks_utils, UI_utils

# Konfiguracja Mediapipe do detekcji dłoni
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
# Nazwa pliku CSV do zapisu współrzędnych
csv_filename = "landmarks.csv"






# Inicjalizacja kamery
picam2 = camera_utils.initialize_camera()

try:
        while True:
            cam_frame = camera_utils.capture_camera_frame(picam2)
            cam_frame_rgb = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            processing_results = hands.process(cam_frame_rgb)
            
            if processing_results.multi_hand_landmarks:
                landmark_coords = []
                draw_landmarks_utils.draw_landmarks(
                    results=processing_results, 
                    image_to_draw=cam_frame, 
                    landmark_coords=landmark_coords, 
                    drawing_utils=mp_drawing, 
                    hand_connections=mp_hands.HAND_CONNECTIONS,
                    image_width=640, 
                    image_height=480
                )
                
                if UI_utils.check_if_specific_key_pressed_cv2('s',1):
                    detection_utils.save_landmark_coordinates(landmark_coords)
            
            camera_utils.display_cam_frame("Live view", cam_frame)
            
            if UI_utils.check_if_specific_key_pressed_cv2('q',1):
                break
finally:
    camera_utils.release_resources(picam2)
