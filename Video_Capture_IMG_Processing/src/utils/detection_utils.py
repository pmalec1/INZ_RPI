
# import cv2
# import mediapipe as mp
# 
# # Konfiguracja obiektów Mediapipe
import os

def detecting_hand_lndmrks(hands, cam_frame_to_process):
    """
    Funkcja do detekcji landmarków dłoni. Przetwarza obraz i zwraca wynik detekcji.
    """
    cam_frame_to_process = cv2.cvtColor(cam_frame_to_process, cv2.COLOR_BGR2RGB)
    return hands.process(cam_frame_to_process)

def check_if_hand_is_detected(processed_frame):
    """
    Funkcja sprawdza, czy na obrazie wykryto dłoń, na podstawie wyniku przetwarzania Mediapipe.
    """
    return processed_frame.multi_hand_landmarks is not None

# Funkcja do zapisu współrzędnych landmarków do pliku CSV
def save_landmark_coordinates(landmark_coords, filename="landmarks.csv"):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("Landmark Coordinates\n")
            f.write(",".join([f"x{i},y{i}" for i in range(21)]) + "\n")
    
    with open(filename, "r") as f:
        lines = f.readlines()

    if len(lines) > 1002:
        lines = lines[:2] + lines[3:]

    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
        f.write(",".join([f"{coord[0]},{coord[1]}" for coord in landmark_coords]) + "\n")
        
    print("Zapisano")