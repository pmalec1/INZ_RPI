from picamera2 import Picamera2, Preview
import time
import cv2

import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils




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

def draw_landmarks(processing_results, image_to_draw):
    for handLandmarks in processing_results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image_to_draw, handLandmarks, mp_hands.HAND_CONNECTIONS)

def display_cam_frame(window_name, frame):
    cv2.imshow(str(window_name), frame)

def check_if_specific_key_pressed_cv2(key_sign):
    # Konwertuje znak klawisza na jego kod ASCII do porównania
    return cv2.waitKey(1) & 0xFF == ord(key_sign)

picam2 = initialize_camera()

try:
    with mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
        while True:
            cam_frame = capture_camera_frame(picam2)          
            processing_results = detecting_hand_lndmrks(cam_frame)
            if check_if_hand_is_detected(processing_results) == True:
                draw_landmarks(processing_results, cam_frame)
            display_cam_frame("Live view", cam_frame) 
            if check_if_specific_key_pressed_cv2('q'):
                break
finally:
            release_resources(picam2)

