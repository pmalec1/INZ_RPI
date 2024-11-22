import cv2


import cv2

def draw_landmarks(image_to_draw, landmark_coords, hand_connections=None):
    """
    Funkcja do rysowania landmarków dłoni na obrazie.
    - image_to_draw: obraz, na którym będą rysowane landmarki.
    - landmark_coords: lista współrzędnych landmarków (x, y).
    - hand_connections: połączenia pomiędzy landmarkami (opcjonalne).
    """
    # Rysowanie punktów landmarków
    for lm_idx, (x, y) in enumerate(landmark_coords):
        # Rysowanie punktu na obrazie
        cv2.circle(image_to_draw, (x, y), 2, (0, 0,0), -1)
        # Rysowanie numeru landmarka na obrazie
        cv2.putText(image_to_draw, str(lm_idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Rysowanie połączeń między landmarkami, jeśli są podane
    if hand_connections:
        for start_idx, end_idx in hand_connections:
            start_point = landmark_coords[start_idx]
            end_point = landmark_coords[end_idx]
            cv2.line(image_to_draw, start_point, end_point, (0, 0, 0), 2)  # Niebieskie linie
