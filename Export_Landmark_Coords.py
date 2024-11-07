from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as ny
import os
import mediapipe as mp




mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

csv_filename = "landmarks.csv"


def initialize_camera():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.start()
    return picam2

def release_resources(picam2):
    picam2.stop()
    cv2.destroyAllWindows()

def capture_camera_frame(picam2):
    return picam2.capture_array()

def detecting_hand_lndmrks(cam_frame_to_process):
     cam_frame_to_process = cv2.cvtColor(cam_frame_to_process, cv2.COLOR_BGR2RGB)
     return hands.process(cam_frame_to_process)

def check_if_hand_is_detected(processed_frame):
    if processing_results.multi_hand_landmarks != None:
        return True
    else :
        return False

def draw_landmarks(results, image_to_draw, landmark_coords):
    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(image_to_draw, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Pobieranie współrzędnych landmarków (X, Y), wyświetlanie numerów landmarków i rysowanie ich jednocześnie
        for lm_idx, lm in enumerate(hand_landmarks.landmark):
            x = int(lm.x * 640)  # Przekształcenie do współrzędnych w pikselach
            y = int(lm.y * 480)
            landmark_coords.append((x, y))  # Dodajemy współrzędne do listy

            # Rysowanie numeru landmarka na obrazie
            cv2.putText(image_to_draw, str(lm_idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
def display_cam_frame(window_name, frame):
    cv2.imshow(str(window_name), frame)

def check_if_specific_key_pressed_cv2(key_sign):
    # Konwertuje znak klawisza na jego kod ASCII do porównania
    return cv2.waitKey(1) & 0xFF == ord(key_sign)

#
#
#

def save_landmark_coordinates(landmark_coords, filename="landmarks.csv"):
    if not os.path.exists(filename):  # Jeśli plik nie istnieje, utwórz go i dodaj nagłówki
        with open(filename, "w") as f:
            f.write("Landmark Coordinates\n")  # Pierwsza linia nagłówka
            # Druga linia nagłówka z nazwami x0 y0 x1 y1 ... x20 y20
           
    
    # Odczytaj dane z pliku, aby sprawdzić liczbę zapisanych linii
    with open(filename, "r") as f:
        lines = f.readlines()

    # Nadpisywanie najstarszych danych po osiągnięciu 1000 zapisów
    if len(lines) > 1002:  # Uwzględniamy dwie linie nagłówka, stąd 1002
        lines = lines[:2] + lines[3:]  # Usunięcie trzeciej linii (najs
      # Dopisanie nowych danych
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
        # Dodanie nowych współrzędnych w jednej linii oddzielonych spacją
        f.write(",".join([f"{coord[0]},{coord[1]}" for coord in landmark_coords]) + "\n")  
        
    print("zapisano")


picam2 = initialize_camera()

try:
    with mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        while True:
            cam_frame = capture_camera_frame(picam2)          
            processing_results = detecting_hand_lndmrks(cam_frame)
            if check_if_hand_is_detected(processing_results) == True:
                landmark_coords = []
                draw_landmarks(processing_results, cam_frame, landmark_coords)
                if check_if_specific_key_pressed_cv2('s'):
                    save_landmark_coordinates(landmark_coords)
            display_cam_frame("Live view", cam_frame)
            
            if check_if_specific_key_pressed_cv2('q'):
                break
finally:
            release_resources(picam2)


