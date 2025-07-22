# modules/modello_lstm.py

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def costruisci_modello(timesteps, features, output_size=11):
    """
    Costruisce un modello LSTM multi-output.
    
    :param timesteps: Numero di estrazioni precedenti da usare come input.
    :param features: Numero di caratteristiche per ogni estrazione.
    :param output_size: 10 numeri + numerone = 11 output.
    :return: Modello compilato pronto per l'addestramento.
    """
    input_layer = Input(shape=(timesteps, features), name="input_lstm")
    x = LSTM(128, return_sequences=True)(input_layer)
    x = Dropout(0.2)(x)
    x = LSTM(64)(x)
    x = Dropout(0.2)(x)
    output = Dense(output_size, activation="sigmoid", name="output")(x)

    model = Model(inputs=input_layer, outputs=output)
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])
    return model
