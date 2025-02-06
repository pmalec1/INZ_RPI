from picamera2 import Picamera2, Preview
import cv2

def initialize():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "RGB888"
    return picam2

def display_frame(window_name, frame):
    cv2.imshow(str(window_name), frame)
    return 

def start(picam2,camera_window_name):
    picam2.start()
    display_frame(str(camera_window_name),0)
    
def release_resources(picam2):
    picam2.stop()
    cv2.destroyAllWindows()

def capture_frame(picam2):
    return picam2.capture_array()

