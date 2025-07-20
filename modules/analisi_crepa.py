import pandas as pd
import numpy as np
from collections import Counter
from math import log2

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
                numeri = eval(numeri)
            except:
                numeri = []
        if not isinstance(numeri, list) or len(numeri) != 10:
            continue  # Salta righe malformate
        entropia = calcola_entropia(numeri)
        entropie.append(entropia)
    return entropie
