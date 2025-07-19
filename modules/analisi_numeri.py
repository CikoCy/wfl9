def calcola_statistiche(df):
    numeri_stats = {n: {"predetti": 0, "indovinati": 0} for n in range(1, 21)}

    for i in range(1, len(df)):
        predetti = df.iloc[i - 1]["10 Numeri"]
        reali = df.iloc[i]["10 Numeri"]

        for num in predetti:
            numeri_stats[num]["predetti"] += 1
            if num in reali:
                numeri_stats[num]["indovinati"] += 1

    # Calcolo tasso di successo per ciascun numero
    pesi = {}
    for n, stat in numeri_stats.items():
        if stat["predetti"] == 0:
            pesi[n] = 0.1  # base minima
        else:
            ratio = stat["indovinati"] / stat["predetti"]
            pesi[n] = max(0.1, round(ratio, 3))  # minimo 0.1

    return pesi

import random

def predict_next_intelligente(pesi, k=10):
    numeri = list(pesi.keys())
    probabilita = list(pesi.values())
    scelti = random.choices(numeri, weights=probabilita, k=50)
    # Elimina duplicati e restituisce primi 10
    unici = []
    for n in scelti:
        if n not in unici:
            unici.append(n)
        if len(unici) == k:
            break
    return unici


def calcola_pesi_numerone(df):
    stats = {n: {"predetti": 0, "indovinati": 0} for n in range(1, 21)}

    for i in range(1, len(df)):
        pred = df.iloc[i - 1]["Numerone"]
        reale = df.iloc[i]["Numerone"]

        stats[pred]["predetti"] += 1
        if pred == reale:
            stats[pred]["indovinati"] += 1

    pesi = {}
    for n in stats:
        p = stats[n]
        if p["predetti"] == 0:
            pesi[n] = 0.1
        else:
            pesi[n] = max(0.1, round(p["indovinati"] / p["predetti"], 3))

    return pesi

import random

def scegli_numerone_intelligente(pesi):
    return random.choices(list(pesi.keys()), weights=list(pesi.values()), k=1)[0]

