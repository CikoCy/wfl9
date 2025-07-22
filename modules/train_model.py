# modules/train_model.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from modello_lstm import costruisci_modello
import os

# === Parametri LSTM ===
TIMESTEPS = 10     # Quante estrazioni guardare indietro
FEATURES = 20      # Ogni estrazione ha 20 numeri (da 1 a 20 in one-hot)
OUTPUT_SIZE = 11   # 10 numeri + numerone

# === Percorsi ===
STORICO_PATH = "dati/storico.csv"
MODEL_PATH = "dati/modello_lstm.h5"

def one_hot_encode_estrazione(estrazione):
    vettore = np.zeros(20)
    for n in estrazione:
        if 1 <= n <= 20:
            vettore[n - 1] = 1
    return vettore

def carica_dati_lstm(path=STORICO_PATH):
    df = pd.read_csv(path)
    sequenze = []
    target = []

    for i in range(TIMESTEPS, len(df)):
        blocco = df.iloc[i - TIMESTEPS:i]
        X_seq = np.array([one_hot_encode_estrazione([int(x) for x in r["10 Numeri"].split(",")]) for _, r in blocco.iterrows()])
        y = df.iloc[i]
        y_estratti = [int(x) for x in y["10 Numeri"].split(",")]
        y_numerone = int(y["Numerone"])
        y_output = np.zeros(11)
        for idx, n in enumerate(y_estratti):
            if 1 <= n <= 20:
                y_output[idx] = (n - 1) / 19  # normalizza tra 0 e 1
        y_output[10] = (y_numerone - 1) / 19
        sequenze.append(X_seq)
        target.append(y_output)

    return np.array(sequenze), np.array(target)

def train_model():
    print("📥 Caricamento dati...")
    X, y = carica_dati_lstm()
    print("✅ Dati caricati:", X.shape, y.shape)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)

    print("🧠 Costruzione modello...")
    model = costruisci_modello(TIMESTEPS, FEATURES, OUTPUT_SIZE)

    os.makedirs("dati", exist_ok=True)

    checkpoint = ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor="val_loss", mode="min")
    early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

    print("🚀 Allenamento in corso...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=[early_stop, checkpoint],
        verbose=1
    )

    print("✅ Modello salvato in:", MODEL_PATH)

if __name__ == "__main__":
    train_model()
