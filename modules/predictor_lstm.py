# modules/predictor_lstm.py

import numpy as np
from tensorflow.keras.models import load_model
import os

MODEL_PATH = "dati/modello_lstm.h5"

def carica_modello():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("❌ Il file modello_lstm.h5 non esiste.")
    model = load_model(MODEL_PATH)
    return model

def one_hot_encode_estrazione(estrazione):
    vettore = np.zeros(20)
    for n in estrazione:
        if 1 <= n <= 20:
            vettore[n - 1] = 1
    return vettore

def prepara_input(df, timesteps=10):
    # Filtra solo righe REALE
    df = df[df["Topo"].str.upper() == "REALE"].reset_index(drop=True)
    
    # Prendi le ultime TIMESTEPS righe
    blocco = df.iloc[-timesteps:]
    X_seq = np.array([
        one_hot_encode_estrazione(eval(r["10 Numeri"]))
        for _, r in blocco.iterrows()
    ])
    X_seq = np.expand_dims(X_seq, axis=0)  # aggiunge dimensione batch
    return X_seq

def denormalizza_output(predizione):
    # Da 0–1 a 1–20
    predizione = np.clip(predizione, 0, 1)
    predizione = np.round(predizione * 19 + 1).astype(int)
    numeri = list(predizione[:10])
    numerone = int(predizione[10])
    
    # Rimuove duplicati nei 10 numeri
    numeri = list(dict.fromkeys(numeri))  # rimuove doppioni mantenendo ordine
    while len(numeri) < 10:
        # Aggiungi numeri casuali non presenti
        candidato = np.random.randint(1, 21)
        if candidato not in numeri:
            numeri.append(candidato)
    return sorted(numeri), numerone

def fai_previsione(df):
    modello = carica_modello()
    X_input = prepara_input(df)
    predizione = modello.predict(X_input, verbose=0)[0]
    numeri, numerone = denormalizza_output(predizione)
    return numeri, numerone
