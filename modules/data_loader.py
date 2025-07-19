
import pandas as pd
import os

FILE = "storico.csv"

def load_storico():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["Estrazione", "Data", "Ora", "10 Numeri", "Numerone"])
        df.to_csv(FILE, index=False)
    df = pd.read_csv(FILE)
    if not df.empty:
        df["10 Numeri"] = df["10 Numeri"].apply(lambda x: list(map(int, str(x).strip("[]").split())))
    return df
