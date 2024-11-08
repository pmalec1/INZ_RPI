import cv2

def draw_landmarks(results, image_to_draw, landmark_coords, drawing_utils, hand_connections, image_width, image_height):
    """
    Funkcja do rysowania landmarków dłoni na obrazie. 
    """
    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        # Rysowanie połączeń dłoni przy użyciu przekazanych funkcji i parametrów
        drawing_utils.draw_landmarks(image_to_draw, hand_landmarks, hand_connections)
        
        # Pobieranie współrzędnych landmarków (X, Y) i wyświetlanie numerów landmarków
        for lm_idx, lm in enumerate(hand_landmarks.landmark):
            x = int(lm.x * image_width)  # Przekształcenie do współrzędnych w pikselach
            y = int(lm.y * image_height)
            landmark_coords.append((x, y))

            # Rysowanie numeru landmarka na obrazie
            cv2.putText(image_to_draw, str(lm_idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
