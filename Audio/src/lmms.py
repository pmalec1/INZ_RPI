import mido
from mido import Message
from pynput import keyboardnnnnnnnn
import random
import time

# Otwórz port MIDI (np. Midi Through Port-0)
outport = mido.open_output('Midi Through Port-0')


def play_random_note():
    # Losowa nuta między 60 (C4) a 72 (C5)
    note = random.randint(60, 100)
    print(f"Granie nuty: {note}")
    
    # Wysłanie komunikatu Note On
    outport.send(Message('note_on', note=note, velocity=100))
    time.sleep(1)  # Trzymaj nutę przez 1 sekundę
    # Wysłanie komunikatu Note Off
    outport.send(Message('note_off', note=note))

# Funkcja nasłuchująca naciśnięcia klawisza
def on_press(key):
    try:
        if key.char == 'n':  # Jeśli naciśnięto klawisz "n"
            play_random_note()n
    except AttributeError:
        pass  # Ignoruj klawisze specjalne

# Uruchom nasłuchiwanie klawiatury
with keyboard.Listener(on_press=on_press) as listener:
    print("Nasłuchuję klawisza 'n'... Naciśnij Ctrl+C, aby zakończyć.")
    listener.join()
