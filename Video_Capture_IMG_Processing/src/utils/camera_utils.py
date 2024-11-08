from picamera2 import Picamera2, Preview
import cv2

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

def display_cam_frame(window_name, frame):
    cv2.imshow(str(window_name), frame)