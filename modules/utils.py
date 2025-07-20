
import pandas as pd
from datetime import datetime, timedelta

def confronto_estrazione(df, numeri, numerone):
    if df.empty or len(df) < 2:
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

def aggiungi_estrazione(df, numeri, numerone, nuova, tipo="REALE"):
    nuova_riga = {
        "Estrazione": nuova["estrazione"],
        "Data": nuova["data"],
        "Ora": nuova["ora"],
        "10 Numeri": numeri,
        "Numerone": numerone,
        "Tipo": tipo
    }
    df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
    df.to_csv("storico.csv", index=False)


from datetime import datetime, timedelta

def genera_data_ora(df):
    if df.empty:
        return {"estrazione": 1, "data": "19/07/2025", "ora": "07:00"}
    
    ultima = df.iloc[-1]
    estrazione = int(ultima["Estrazione"]) + 1

    # 🔄 Calcola data e ora
    data = datetime.strptime(f"{ultima['Data']} {ultima['Ora']}", "%d/%m/%Y %H:%M")
    data += timedelta(hours=1)
    if data.hour > 23:
        data += timedelta(days=1)
        data = data.replace(hour=7)

    return {
        "estrazione": estrazione,
        "data": data.strftime("%d/%m/%Y"),
        "ora": data.strftime("%H:%M")
    }


def aggiorna_diario(df, numeri, numerone, nuova):
    with open("diario.txt", "a") as f:
        f.write(f"[{nuova['estrazione']}] {nuova['data']} {nuova['ora']} => {numeri} + Numerone {numerone}\n")
        confronto = confronto_estrazione(df, numeri, numerone)
        f.write(f" --> Match: {confronto['match']} numeri, Numerone: {'✔️' if confronto['numerone_match'] else '❌'}\n\n")


def rendi_10_univoci(numeri_predetti):
    numeri_finali = []
    visti = set()

    for n in numeri_predetti:
        if n not in visti:
            numeri_finali.append(n)
            visti.add(n)
        if len(numeri_finali) == 10:
            break

    for n in range(1, 21):
        if len(numeri_finali) == 10:
            break
        if n not in visti:
            numeri_finali.append(n)

    return numeri_finali

