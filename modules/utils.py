
import pandas as pd
from datetime import datetime, timedelta

def confronto_estrazione(df, numeri, numerone):
    if df.empty:
        return {"match": 0, "numerone_match": False, "dettaglio": {}}
    last_pred = df.iloc[-2]["10 Numeri"]
    last_num = df.iloc[-2]["Numerone"]
    match = len(set(last_pred) & set(numeri))
    num_match = (last_num == numerone)
    return {
        "match": match,
        "numerone_match": num_match,
        "dettaglio": {
            "numeri_predetti": last_pred,
            "numeri_reali": numeri,
            "numerone_predetto": last_num,
            "numerone_reale": numerone
        }
    }

def aggiungi_estrazione(df, numeri, numerone, nuova):
    nuova_riga = {
        "Estrazione": nuova["estrazione"],
        "Data": nuova["data"],
        "Ora": nuova["ora"],
        "10 Numeri": numeri,
        "Numerone": numerone
    }
    df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
    df.to_csv("storico.csv", index=False)

def genera_data_ora(df):
    if df.empty:
        return {"estrazione": 1, "data": "2025-07-19", "ora": "07:00"}
    ultima = df.iloc[-1]
    estrazione = int(ultima["Estrazione"]) + 1
    data = datetime.strptime(f"{ultima['Data']} {ultima['Ora']}", "%d/%m/%Y %H:%M")
    data += timedelta(hours=1)
    if data.hour > 23:
        data += timedelta(days=1)
        data = data.replace(hour=7)
    return {"estrazione": estrazione, "data": data.strftime("%Y-%m-%d"), "ora": data.strftime("%H:%M")}

def aggiorna_diario(df, numeri, numerone, nuova):
    with open("diario.txt", "a") as f:
        f.write(f"[{nuova['estrazione']}] {nuova['data']} {nuova['ora']} => {numeri} + Numerone {numerone}\n")
