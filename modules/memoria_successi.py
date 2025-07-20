def analizza_successi(df):
    """
    Conta quante volte ogni numero è stato indovinato nelle previsioni.
    """
    successi = {n: 0 for n in range(1, 21)}

    if "Tipo" not in df.columns or len(df) < 2:
        return successi

    for i in range(1, len(df)):
        riga_prev = df.iloc[i - 1]
        riga_reale = df.iloc[i]

        if riga_prev["Tipo"] == "PREVISIONE" and riga_reale["Tipo"] == "REALE":
            predetti = set(riga_prev["10 Numeri"])
            reali = set(riga_reale["10 Numeri"])

            presi = predetti & reali
            for n in presi:
                successi[n] += 1

    return successi
