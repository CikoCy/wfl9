
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

MODEL_PATH = "model_sklearn.pkl"

def train_model(df):
    if df.empty or len(df) < 10:
        return None
    X = []
    y = []
    for i in range(len(df)-1):
        current = df.iloc[i]["10 Numeri"]
        target = df.iloc[i+1]["10 Numeri"]
        X.append(current)
        y.append(target[0])  # solo primo numero come esempio semplice
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

def predict_next(model, df):
    if model is None or df.empty:
        return [], 0
    X = [df.iloc[-1]["10 Numeri"]]
    pred = model.predict(X)[0]
    pred_numeri = sorted(set([pred] + list(np.random.choice(range(1, 21), 9, replace=False))))
    pred_numerone = int(np.random.choice(range(1, 21)))
    return pred_numeri[:10], pred_numerone

def save_model(model):
    joblib.dump(model, MODEL_PATH)

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)
