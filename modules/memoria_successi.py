import pandas as pd
import os
import ast

def analizza_successi(df):
    """
    Conta quante volte ogni numero è stato INDOVINATO nelle previsioni.
    """
    successi = {n: 0 for n in range(1, 21)}

    if "Tipo" not in df.columns or len(df) < 2:
        return successi

    for i in range(1, len(df)):
        riga_prev = df.iloc[i - 1]
        riga_reale = df.iloc[i]

        if riga_prev["Tipo"] == "PREVISIONE" and riga_reale["Tipo"] == "REALE":
            predetti = riga_prev["10 Numeri"]
            reali = riga_reale["10 Numeri"]

            if isinstance(predetti, str):
                try:
                    predetti = ast.literal_eval(predetti)
                except:
                    predetti = []
            if isinstance(reali, str):
                try:
                    reali = ast.literal_eval(reali)
                except:
                    reali = []

            presi = set(predetti) & set(reali)
            for n in presi:
                if n in successi:
                    successi[n] += 1

    return successi

def analizza_successi_numerone(df):
    """
    Conta quante volte ogni numerone è stato INDOVINATO.
    """
    successi = {n: 0 for n in range(1, 21)}

    if "Tipo" not in df.columns or len(df) < 2:
        return successi

    for i in range(1, len(df)):
        riga_prev = df.iloc[i - 1]
        riga_reale = df.iloc[i]

        if riga_prev["Tipo"] == "PREVISIONE" and riga_reale["Tipo"] == "REALE":
            predetto = riga_prev["Numerone"]
            reale = riga_reale["Numerone"]

            if predetto == reale and predetto in successi:
                successi[predetto] += 1

    return successi

def salva_successi(successi):
    os.makedirs("dati", exist_ok=True)
    df = pd.DataFrame({
        "Numero": list(successi.keys()),
        "Successi": list(successi.values())
    })
    df.to_csv("dati/memoria_successi.csv", index=False)

def salva_successi_numerone(successi_n):
    os.makedirs("dati", exist_ok=True)
    df = pd.DataFrame({
        "Numerone": list(successi_n.keys()),
        "Successi": list(successi_n.values())
    })
    df.to_csv("dati/memoria_successi_numerone.csv", index=False)
