from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np
import os
import mediapipe as mp
from utils import camera_utils, detection_utils, draw_landmarks_utils, UI_utils, landmarks_processing

# Konfiguracja Mediapipe do detekcji dłoni
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
# Nazwa pliku CSV do zapisu współrzędnych
csv_filename = "data/Training_Data/down_open_fist_front.csv"
csv_file = None  # Zmienna do przechowywania uchwytu pliku

# Inicjalizacja kamery
picam2 = camera_utils.initialize_camera()
try:
    csv_file = open(csv_filename, "a")
    while (UI_utils.check_if_specific_key_pressed_cv2('q',1)==False):
        
        cam_frame = camera_utils.capture_camera_frame(picam2)
        processing_results=detection_utils.detecting_hand_lndmrks(hands,cam_frame)        
        
        if detection_utils.check_if_hand_is_detected(processing_results):
            
            landmark_coords = landmarks_processing.process_one_hand_landmarks_coords(processing_results.multi_hand_landmarks,640, 480)
            roi=landmarks_processing.calculate_roi(landmark_coords)
            normalized_lndms_coords=landmarks_processing.normalize_landmarks(landmark_coords,roi)
            draw_landmarks_utils.draw_landmarks(cam_frame,landmark_coords,mp_hands.HAND_CONNECTIONS)

            if UI_utils.check_if_specific_key_pressed_cv2('s',1)==True:
                landmarks_processing.save_landmark_coordinates(normalized_lndms_coords, csv_filename) 
    
        camera_utils.display_cam_frame("Live view", cam_frame)
    
finally:
    
    camera_utils.release_resources(picam2)
    if csv_file:
        csv_file.close()
        print(f"Plik {csv_filename} został zamknięty.")
