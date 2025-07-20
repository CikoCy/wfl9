import pandas as pd

def analizza_errori(df):
    """
    Analizza lo storico per contare quante volte ogni numero NON è stato indovinato
    nelle previsioni confrontate con le estrazioni reali.
    """
    errori = {n: 0 for n in range(1, 21)}

    # Serve almeno una previsione + una reale
    if "Tipo" not in df.columns or len(df) < 2:
        return errori

    # Scorri tutte le righe per coppie PREVISIONE + REALE
    for i in range(1, len(df)):
        riga_prev = df.iloc[i-1]
        riga_reale = df.iloc[i]

        if riga_prev["Tipo"] == "PREVISIONE" and riga_reale["Tipo"] == "REALE":
            predetti = set(riga_prev["10 Numeri"])
            reali = set(riga_reale["10 Numeri"])

            non_presi = predetti - reali
            for n in non_presi:
                errori[n] += 1

    return errori
