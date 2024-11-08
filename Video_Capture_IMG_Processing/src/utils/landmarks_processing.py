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

# Funkcja normalizująca współrzędne względem ROI
def normalize_landmarks(landmark_coords):
    x_coords = [coord[0] for coord in landmark_coords]
    y_coords = [coord[1] for coord in landmark_coords]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    width = max_x - min_x
    height = max_y - min_y

    normalized_landmarks = [((x - min_x) / width, (y - min_y) / height) for (x, y) in landmark_coords]
    roi = (min_x, min_y, max_x, max_y)
    return normalized_landmarks, roi





