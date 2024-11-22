
import cv2
import mediapipe as mp
# 
# # Konfiguracja obiektów Mediapipe
import os

def detecting_hand_lndmrks(hands,cam_frame):
    cam_frame_rgb = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
    processing_results = hands.process(cam_frame_rgb)
    return processing_results

def check_if_hand_is_detected(processing_results):
    """
    Funkcja sprawdza, czy na obrazie wykryto dłoń, na podstawie wyniku przetwarzania Mediapipe.
    """
    return processing_results.multi_hand_landmarks is not None

