import pandas as pd
import numpy as np
from collections import Counter
from math import log2
import ast
import os

def calcola_entropia(estrazione):
    counter = Counter(estrazione)
    totale = sum(counter.values())
    if totale == 0:
        return 0
    return -sum((c / totale) * log2(c / totale) for c in counter.values())

def analizza_entropia(df):
    entropie = []
    for i, row in df.iterrows():
        numeri = row["10 Numeri"]
        if isinstance(numeri, str):
            try:
                numeri = ast.literal_eval(numeri)
            except:
                numeri = []
        if not isinstance(numeri, list) or len(numeri) != 10:
            continue  # Salta righe malformate
        entropia = calcola_entropia(numeri)
        entropie.append({
            "Estrazione": row["Estrazione"],
            "Data": row["Data"],
            "Ora": row["Ora"],
            "Entropia": entropia
        })
    return pd.DataFrame(entropie)

def salva_entropie(df_entropie):
    os.makedirs("dati", exist_ok=True)
    df_entropie.to_csv("dati/entropie.csv", index=False)
