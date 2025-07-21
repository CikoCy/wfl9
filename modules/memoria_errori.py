import pandas as pd

def analizza_errori(df):
    """
    Analizza lo storico per contare quante volte ogni numero NON è stato indovinato
    nelle previsioni confrontate con le estrazioni reali.
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

            # Sicurezza: assicurati che siano liste
            if isinstance(predetti, str):
                try:
                    predetti = eval(predetti)
                except:
                    predetti = []
            if isinstance(reali, str):
                try:
                    reali = eval(reali)
                except:
                    reali = []

            predetti_set = set(predetti)
            reali_set = set(reali)

            non_presi = predetti_set - reali_set
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
