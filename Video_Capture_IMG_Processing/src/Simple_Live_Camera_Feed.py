from picamera2 import Picamera2, Preview
import time
import cv2

#Inicjalizacja kamery
picam2 = Picamera2()
#Konfiguracja kamery
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
#Uruchomienie kamery
picam2.start()

try:
    while True:
        frame = picam2.capture_array()
        cv2.imshow("Live camera feed", frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
finally:
        picam2.stop()
        cv2.destroyAllWindows()
