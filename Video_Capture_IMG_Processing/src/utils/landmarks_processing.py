import csv
import os
import numpy as np


# Ścieżka do pliku CSV
csv_filename = "landmarks.csv"




# Funkcja odczytująca współrzędne landmarków z CSV
def read_landmark_coordinates_from_csv(filename, line_number):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = list(reader)
        if line_number + 2 < len(lines):
            landmarks = lines[line_number + 2]  # Pomijamy 2 linie nagłówka
            landmark_coords = [(float(landmarks[i]), float(landmarks[i+1])) for i in range(0, len(landmarks), 2)]
            return landmark_coords
        else:
            print("Nie ma tylu linii w pliku.")
            return None



def calculate_roi(landmark_coords):
    x_coords = [coord[0] for coord in landmark_coords]
    y_coords = [coord[1] for coord in landmark_coords]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    return min_x, min_y, max_x, max_y


def calculate_roi_center(roi):
    min_x, min_y, max_x, max_y = roi
    # Obliczanie środka z zaokrągleniem do liczb całkowitych
    center_x = round((min_x + max_x) / 2)
    center_y = round((min_y + max_y) / 2)
    return center_x, center_y

def normalize_landmarks(landmark_coords, roi):

    min_x, min_y, max_x, max_y = roi

    # Obliczanie szerokości i wysokości ROI
    width = max_x - min_x
    height = max_y - min_y

    # Normalizowanie współrzędnych względem ROI z precyzją 4 miejsc po przecinku
    normalized_landmarks = [
        (f"{(x - min_x) / width:.4f}", f"{(y - min_y) / height:.4f}") for (x, y) in landmark_coords
    ]

    return normalized_landmarks





def process_one_hand_landmarks_coords(multi_hand_landmarks, image_width, image_height):

    # Pobranie pierwszej dłoni
    first_hand_landmarks = multi_hand_landmarks[0]
    
    # Lista na współrzędne
    landmark_coords = []
    
    # Przetworzenie każdego landmarka
    for landmark in first_hand_landmarks.landmark:
        x = int(landmark.x * image_width)
        y = int(landmark.y * image_height)
        landmark_coords.append((x, y))
    
    return landmark_coords


def save_landmark_coordinates(landmark_coords, filename):
  
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)

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
        
    print(f"Zapisano dane do pliku: {filename}")
