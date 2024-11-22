import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# Funkcja do wczytywania danych gestów
def load_gesture_data(filenames, labels):
    """
    Ładuje dane gestów z plików CSV i przypisuje etykiety.
    filenames: lista plików CSV
    labels: lista etykiet odpowiadających plikom
    Zwraca: połączone dane i etykiety
    """
    gesture_data = []
    gesture_labels = []
    for filename, label in zip(filenames, labels):
        data = pd.read_csv(filename, header=None).values  # Wczytaj dane z CSV
        gesture_data.append(data)  # Dodaj dane gestu
        gesture_labels.append(np.full(data.shape[0], label))  # Dodaj etykiety
    return np.vstack(gesture_data), np.hstack(gesture_labels)  # Połącz wszystkie dane i etykiety

# Lista plików CSV z danymi gestów
gesture_files = [
    "data/Training_Data/up_open_fist_front.csv",
    "data/Training_Data/down_open_fist_front.csv",
    "data/Training_Data/thumb_up.csv"
]
labels = [0, 1, 2]  # Etykiety dla gestów (0, 1, 2)

# Wczytaj dane i etykiety
X, y = load_gesture_data(gesture_files, labels)

# Podział na zbiory treningowy i walidacyjny
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizacja danych
X_train = X_train.astype('float32')
X_val = X_val.astype('float32')

# One-hot encoding dla etykiet
num_classes = len(labels)
y_train = to_categorical(y_train, num_classes=num_classes)
y_val = to_categorical(y_val, num_classes=num_classes)

# Tworzenie modelu sieci neuronowej z jedną warstwą ukrytą
model = Sequential([
    Dense(32, activation='relu', input_shape=(42,)),  # Jedyna warstwa ukryta
    Dense(num_classes, activation='softmax')  # Warstwa wyjściowa
])

# Kompilowanie modelu
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# EarlyStopping - zatrzymanie, gdy walidacyjna strata się nie poprawia
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Trenowanie modelu
model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,  # Liczba maksymalnych epok
    batch_size=16,  # Rozmiar partii
    callbacks=[early_stopping]  # Automatyczne zatrzymanie
)

# Zapis modelu do pliku
model.save("gesture_model.h5")
print("Model został zapisany.")
