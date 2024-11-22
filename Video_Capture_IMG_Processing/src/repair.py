from picamera2 import Picamera2
import cv2

# Inicjalizacja kamery
picam2 = Picamera2()

# Konfiguracja trybu podglądu
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)

# Start kamery
picam2.start()

# Przechwytywanie jednej klatki
frame = picam2.capture_array()

# Wyświetlanie obrazu
cv2.imshow("Captured Frame", frame)

# Zapisywanie obrazu do pliku
cv2.imwrite("captured_frame.jpg", frame)

# Czekaj na klawisz ESC, aby zamknąć okno
print("Press ESC to close.")
while True:
    if cv2.waitKey(1) & 0xFF == 27:  # Kod klawisza ESC
        break

# Zamykanie okien i zatrzymanie kamery
cv2.destroyAllWindows()
picam2.stop()
