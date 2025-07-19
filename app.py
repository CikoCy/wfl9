
import streamlit as st
from modules.data_loader import load_storico
from modules.model_sklearn import train_model, predict_next, save_model, load_model
from modules.utils import confronto_estrazione, aggiungi_estrazione, genera_data_ora, aggiorna_diario

st.set_page_config(page_title="WFL 9.0", layout="centered", initial_sidebar_state="collapsed")
st.title("🔮 WFL 9.0 - Previsione Win for Life")

st.markdown("### 📥 Caricamento storico")
df = load_storico()

if df.empty:
    st.warning("Il file storico è vuoto. Aggiungi la prima estrazione.")
else:
    st.dataframe(df.tail(3))

model = load_model()
if model is None:
    model = train_model(df)
    save_model(model)

st.markdown("### 🤖 Previsione automatica")
if st.button("Genera Previsione"):
    pred_numeri, pred_numerone = predict_next(model, df)
    st.success(f"Numeri Previsti: {pred_numeri}")
    st.info(f"Numerone Previsto: {pred_numerone}")

st.markdown("### 🎯 Inserisci nuova estrazione reale")
estrazione_input = st.text_input("Inserisci i 10 numeri + numerone separati da spazio (es: 1 2 3 4 5 6 7 8 9 10 15)")
if estrazione_input:
    try:
        estratti = list(map(int, estrazione_input.strip().split()))
        if len(estratti) != 11:
            st.error("Devi inserire esattamente 10 numeri + 1 numerone.")
        else:
            numeri, numerone = estratti[:10], estratti[10]
            nuova_estrazione = genera_data_ora(df)
            aggiorna_diario(df, numeri, numerone, nuova_estrazione)
            aggiungi_estrazione(df, numeri, numerone, nuova_estrazione)
            save_model(train_model(df))
            st.success("Estrazione aggiunta e modello aggiornato.")
            confronto = confronto_estrazione(df, numeri, numerone)
            st.json(confronto)
    except Exception as e:
        st.error(f"Errore: {e}")
