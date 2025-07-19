import pandas as pd
import ast

def load_storico(path="storico.csv"):
    try:
        df = pd.read_csv(path)
        if df.empty:
            return None

        # Converte SOLO se serve
        if isinstance(df["10 Numeri"].iloc[0], str):
            df["10 Numeri"] = df["10 Numeri"].apply(ast.literal_eval)

        return df
    except Exception as e:
        print(f"Errore nel caricamento dello storico: {e}")
        return None
