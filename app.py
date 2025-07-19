
import streamlit as st
from modules.data_loader import load_storico
from modules.analisi_numeri import (
    calcola_statistiche,
    predict_next_intelligente,
    calcola_pesi_numerone,
    scegli_numerone_intelligente
)
from modules.utils import confronto_estrazione, aggiungi_estrazione, genera_data_ora, aggiorna_diario
from modules.utils import rendi_10_univoci


st.set_page_config(page_title="WFL 9.0", layout="centered", initial_sidebar_state="collapsed")
st.title("🔮 WFL 9.0 - Previsione Win for Life")

st.markdown("### 📥 Caricamento storico")
df = load_storico()

if df is None or df.empty:
    st.warning("⚠️ Storico vuoto o errore nel caricamento.")
    st.stop()

else:
    st.dataframe(df.tail(3))
    

st.markdown("### 🧠 Previsione Intelligente (basata su successi ed errori)")

if st.button("Genera Previsione Intelligente"):
    pesi_numeri = calcola_statistiche(df)
    pesi_numeroni = calcola_pesi_numerone(df)

    pred_numeri = predict_next_intelligente(pesi_numeri)
    pred_numeri = rendi_10_univoci(pred_numeri)

    pred_numerone = scegli_numerone_intelligente(pesi_numeroni)

    nuova_estrazione = genera_data_ora(df)
    aggiungi_estrazione(df, pred_numeri, pred_numerone, nuova_estrazione)

    st.success(f"✅ Previsione registrata: {sorted(pred_numeri)} + Numerone {pred_numerone}")


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
            st.success("✅ Estrazione reale aggiunta.")
            confronto = confronto_estrazione(df, numeri, numerone)
            st.json(confronto)
    except Exception as e:
        st.error(f"Errore: {e}")


with st.expander("📖 Diario delle estrazioni"):
    try:
        with open("diario.txt", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.info("Il diario è vuoto o non è stato ancora creato.")


