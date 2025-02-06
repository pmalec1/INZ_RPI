import serial
import time

# Konfiguracja portu UART
ser = serial.Serial('/dev/serial0', 9600, timeout=1)  # Główny port UART na RPi
time.sleep(2)  # Opóźnienie na inicjalizację

print("Naciśnij 's' aby wysłać wiadomość 'UART FRAME'. Naciśnij 'q' aby zakończyć.")

try:
    while True:
        user_input = input()  # Odczyt wejścia z klawiatury

        if user_input.lower() == 's':
            ser.write(b'UART FRAME\n')
            print("Wysłano: UART FRAME")

        elif user_input.lower() == 'q':
            print("Zamykanie programu...")
            break  # Przerwij pętlę i zakończ program

except KeyboardInterrupt:
    print("\nProgram zakończony przez użytkownika.")

finally:
    ser.close()
    print("Port UART zamknięty.")
