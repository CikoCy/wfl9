# modules/modulo_auto_ottimizzazione.py
import numpy as np
from collections import Counter
import pandas as pd

def carica_memorie():
    try:
        errori = pd.read_csv("dati/memoria_errori.csv")["Numero"].tolist()
    except:
        errori = []
    try:
        successi = pd.read_csv("dati/memoria_successi.csv")["Numero"].tolist()
    except:
        successi = []

    return errori, successi

def genera_lista_ottimizzata(n=10):
    numeri_possibili = list(range(1, 21))
    pesi = np.ones(20)  # default: ogni numero ha peso 1

    errori, successi = carica_memorie()

    # penalizza errori (-0.3), premia successi (+0.5)
    for i in range(20):
        numero = i + 1
        if numero in errori:
            pesi[i] -= 0.3
        if numero in successi:
            pesi[i] += 0.5

    # evita pesi negativi
    pesi = np.clip(pesi, 0.1, None)

    # normalizza
    pesi /= pesi.sum()

    # estrai numeri unici secondo i pesi ottimizzati
    predizione = np.random.choice(numeri_possibili, size=n, replace=False, p=pesi)
    return sorted(predizione), pesi
