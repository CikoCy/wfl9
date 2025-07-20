import pandas as pd
import ast

def load_storico(path="dati/storico.csv"):
    try:
        df = pd.read_csv(path)

        if df.empty:
            return None

        # Converte i 10 numeri da stringa a lista, se necessario
        if isinstance(df["10 Numeri"].iloc[0], str):
            df["10 Numeri"] = df["10 Numeri"].apply(ast.literal_eval)

        # Assicura che il campo Tipo sia tutto MAIUSCOLO
        if "Tipo" in df.columns:
            df["Tipo"] = df["Tipo"].astype(str).str.upper()

        return df

    except Exception as e:
        print(f"Errore nel caricamento dello storico: {e}")
        return None
