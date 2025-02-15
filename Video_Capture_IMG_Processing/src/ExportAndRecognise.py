from picamera2 import Picamera2
import time
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from utils import camera_utils, detection_utils, draw_landmarks_utils, UI_utils, landmarks_processing

# Konfiguracja Mediapipe do detekcji dłoni
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, 
                       min_detection_confidence=0.7, 
                       min_tracking_confidence=0.7, 
                       max_num_hands=1)

# Ładowanie wytrenowanego modelu
model_path = "gesture_model.h5"  # Ścieżka do pliku modelu
gesture_model = load_model(model_path)
gestures = ["Up Open Fist", "Down Open Fist", "Thumb Up"]  # Nazwy gestów

# Inicjalizacja kamery
picam2 = camera_utils.initialize()
camera_utils.start(picam2, "Live")
try:
    while not UI_utils.check_if_specific_key_pressed_cv2('q', 1):
        # Przechwycenie klatki z kamery
        cam_frame = camera_utils.capture_frame(picam2)

        # Detekcja dłoni za pomocą Mediapipe
        processing_results = detection_utils.detecting_hand_lndmrks(hands, cam_frame)

        if detection_utils.check_if_hand_is_detected(processing_results):
            # Przetwarzanie współrzędnych landmarków
            landmark_coords = landmarks_processing.process_one_hand_landmarks_coords(
                processing_results.multi_hand_landmarks, 640, 480
            )

            if landmark_coords is not None:
                # Obliczanie ROI i normalizacja współrzędnych
                roi = landmarks_processing.calculate_roi(landmark_coords)
                
                if roi is not None:
                    # Konwersja do numpy array w razie potrzeby
                    normalized_lndms_coords = np.array(landmarks_processing.normalize_landmarks(landmark_coords, roi), dtype=np.float32)
                    
                    # Przygotowanie danych do modelu
                    try:
                        input_data = np.array([normalized_lndms_coords.flatten()], dtype=np.float32)
                        probabilities = gesture_model.predict(input_data, verbose=0)[0]  # Predykcja
                        max_prob = np.max(probabilities)
                        predicted_class = np.argmax(probabilities)

                        # Rozpoznawanie gestu lub brak gestu
                        if max_prob > 0.4:  # Jeśli prawdopodobieństwo jest wystarczająco wysokie
                            detected_gesture = gestures[predicted_class]
                        else:
                            detected_gesture = "No gesture detected"

                        # Wyświetlenie wyniku
                        cv2.putText(cam_frame, f"Gesture: {detected_gesture} ({max_prob:.2f})", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        # Rysowanie landmarków na klatce
                        draw_landmarks_utils.draw_landmarks(cam_frame, landmark_coords, mp_hands.HAND_CONNECTIONS)

                    except Exception as e:
                        print(f"Błąd podczas predykcji: {e}")
                else:
                    print("ROI nie zostało poprawnie obliczone.")
            else:
                print("Nie wykryto współrzędnych landmarków.")
        else:
            print("Nie wykryto dłoni.")

        # Wyświetlenie obrazu na żywo
        camera_utils.display_frame("Live view", cam_frame)

finally:
    camera_utils.release_resources(picam2)
    hands.close()
    print("Zasoby zostały zwolnione.")
