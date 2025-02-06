from pynput import keyboard
import mido
import time

# Znajdź port MIDI zawierający "FLUID Synth"
port_name = next(name for name in mido.get_output_names() if 'FLUID Synth' in name)
print(f"Używany port MIDI: {port_name}")

# Otwórz port MIDI
output = mido.open_output(port_name)

volume = 100  # Początkowa głośność (zakres 0-127)

def send_control_change(control, value):
    """Wysyła komunikat Control Change do Qsynth."""
    msg = mido.Message('control_change', control=control, value=value)
    output.send(msg)

def play_note(note=60):
    """Zagraj nutę z aktualną głośnością."""
    msg_on = mido.Message('note_on', note=note, velocity=volume)
    output.send(msg_on)
    time.sleep(0.5)
    msg_off = mido.Message('note_off', note=note)
    output.send(msg_off)

# Funkcje do obsługi klawiszy
def on_press(key):
    global volume
    try:
        if key == keyboard.Key.up:
            if volume < 127:
                volume += 5
                send_control_change(7, volume)  # CC 7: Głośność
                print(f"Głośność: {volume}")
        elif key == keyboard.Key.down:
            if volume > 0:
                volume -= 5
                send_control_change(7, volume)
                print(f"Głośność: {volume}")
        elif key == keyboard.Key.space:
            play_note()
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Zakończ program po wciśnięciu ESC
        print("Zakończono.")
        return False

# Uruchom nasłuchiwanie klawiszy
print("Użyj strzałek, aby zmieniać głośność. Naciśnij 'Space', aby zagrać nutę. ESC, aby zakończyć.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
  