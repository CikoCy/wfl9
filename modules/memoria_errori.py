import pandas as pd
import os
import ast

def analizza_errori(df):
    """
    Conta quante volte ogni numero NON è stato indovinato nelle previsioni confrontate con le estrazioni reali.
    """
    errori = {n: 0 for n in range(1, 21)}

    if "Tipo" not in df.columns or len(df) < 2:
        return errori

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

            non_presi = set(predetti) - set(reali)
            for n in non_presi:
                if n in errori:
                    errori[n] += 1

    return errori

def analizza_errori_numerone(df):
    """
    Conta quante volte ogni numerone è stato SBAGLIATO nelle previsioni.
    """
    errori = {n: 0 for n in range(1, 21)}

    if "Tipo" not in df.columns or len(df) < 2:
        return errori

    for i in range(1, len(df)):
        riga_prev = df.iloc[i - 1]
        riga_reale = df.iloc[i]

        if riga_prev["Tipo"] == "PREVISIONE" and riga_reale["Tipo"] == "REALE":
            predetto = riga_prev["Numerone"]
            reale = riga_reale["Numerone"]

            if predetto != reale and predetto in errori:
                errori[predetto] += 1

    return errori

def salva_errori(errori):
    os.makedirs("dati", exist_ok=True)
    df = pd.DataFrame({
        "Numero": list(errori.keys()),
        "Errori": list(errori.values())
    })
    df.to_csv("dati/memoria_errori.csv", index=False)

def salva_errori_numerone(errori_n):
    os.makedirs("dati", exist_ok=True)
    df = pd.DataFrame({
        "Numerone": list(errori_n.keys()),
        "Errori": list(errori_n.values())
    })
    df.to_csv("dati/memoria_errori_numerone.csv", index=False)
