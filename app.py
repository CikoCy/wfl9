
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
from modules.memoria_errori import analizza_errori
from modules.memoria_successi import analizza_successi



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

    # Se esiste già una previsione, non rigenerare
    if "Tipo" in df.columns and len(df) > 0 and df.iloc[-1]["Tipo"] == "PREVISIONE":
        st.warning("⚠️ Hai già una previsione in attesa di conferma. Inserisci prima l'estrazione reale.")
    else:
        # Calcola pesi solo sulle REALI
        pesi_numeri = calcola_statistiche(df[df["Tipo"] == "REALE"] if "Tipo" in df.columns else df)
        pesi_numeroni = calcola_pesi_numerone(df[df["Tipo"] == "REALE"] if "Tipo" in df.columns else df)

        pred_numeri = predict_next_intelligente(pesi_numeri)
        pred_numeri = rendi_10_univoci(pred_numeri)
        pred_numerone = scegli_numerone_intelligente(pesi_numeroni)

        nuova_estrazione = genera_data_ora(df)
        aggiungi_estrazione(df, pred_numeri, pred_numerone, nuova_estrazione, tipo="PREVISIONE")

        st.success(f"✅ Previsione registrata: {sorted(pred_numeri)} + Numerone {pred_numerone}")



st.markdown("### 🎯 Inserisci nuova estrazione reale")
estrazione_input = st.text_input("Inserisci i 10 numeri + numerone separati da spazio (es: 1 2 3 4 5 6 7 8 9 10 15)")

if estrazione_input:
    try:
        estratti = list(map(int, estrazione_input.strip().split()))
        if len(estratti) != 11:
            st.error("Devi inserire esattamente 10 numeri + 1 numerone.")
        else:
            # ⚠️ Controlla se esiste una previsione da confermare
            if len(df) == 0 or df.iloc[-1]["Tipo"] != "PREVISIONE":
                st.error("❌ Nessuna previsione da confermare. Genera prima una previsione.")
                st.stop()

            # 🔗 Prendi estrazione, data, ora dalla previsione esistente
            ultima = df.iloc[-1]
            nuova_estrazione = {
                "estrazione": ultima["Estrazione"],
                "data": ultima["Data"],
                "ora": ultima["Ora"]
            }

            numeri, numerone = estratti[:10], estratti[10]

            aggiorna_diario(df, numeri, numerone, nuova_estrazione)
            aggiungi_estrazione(df, numeri, numerone, nuova_estrazione, tipo="REALE")
            st.success("✅ Estrazione reale aggiunta e sincronizzata con la previsione.")

            # 🔍 Confronto Intelligente
            confronto = confronto_estrazione(df, numeri, numerone)
            match = confronto["match"]
            numerone_match = confronto["numerone_match"]
            dettaglio = confronto["dettaglio"]
            numeri_predetti = dettaglio["numeri_predetti"]
            numeri_reali = dettaglio["numeri_reali"]
            numeri_indovinati = sorted(list(set(numeri_predetti) & set(numeri_reali)))

            st.markdown("### 📊 Confronto Intelligente")
            st.write("🎯 **Numeri Predetti:**", ", ".join(map(str, sorted(numeri_predetti))))
            st.write("🎯 **Numeri Reali:**", ", ".join(map(str, sorted(numeri_reali))))
            st.write("✅ **Numeri Indovinati:**", ", ".join(map(str, numeri_indovinati)))
            st.markdown("---")
            st.write(f"🔢 **Totale Match:** {match}/10")
            st.write(f"🎯 **Numerone Predetto:** {dettaglio['numerone_predetto']}")
            st.write(f"🎯 **Numerone Reale:** {dettaglio['numerone_reale']}")
            st.markdown(f"💥 **Numerone Match:** {'✔️' if numerone_match else '❌'}")

    except Exception as e:
        st.error(f"Errore: {e}")


with st.expander("📖 Diario delle estrazioni"):
    try:
        with open("diario.txt", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.info("Il diario è vuoto o non è stato ancora creato.")

with st.expander("🧠 Memoria degli Errori"):
    errori = analizza_errori(df)
    st.write("📉 **Errori per numero (orizzontale):**")
    riga = " | ".join([f"{n}: {errori[n]}" for n in range(1, 21)])
    st.markdown(f"`{riga}`")

with st.expander("🎯 Memoria dei Successi"):
    successi = analizza_successi(df)
    riga = " | ".join([f"{n}: {successi[n]}" for n in range(1, 21)])
    st.markdown(f"`{riga}`")


st.markdown("### 📂 Visualizzazione Storico Intelligente")

tipo_filtro = st.selectbox("Filtra per tipo di riga:", options=["TUTTO", "PREVISIONE", "REALE"])

df_filtrato = df.copy()
if "Tipo" in df.columns:
    if tipo_filtro != "TUTTO":
        df_filtrato = df[df["Tipo"] == tipo_filtro]

    st.dataframe(df_filtrato.tail(15), use_container_width=True)
else:
    st.warning("Lo storico attuale non ha la colonna 'Tipo'. Vuoi che la aggiungiamo?")

