import streamlit as st
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI

st.title("📊 Analyse Crypto avec CoinGecko (Données Réelles)")

# Initialiser client CoinGecko
cg = CoinGeckoAPI()

# Sélection de la crypto
crypto = st.text_input("Symbole (ex: bitcoin, ethereum, cardano)", "bitcoin")

# Intervalle en jours
jours = st.slider("Nombre de jours d'historique", 1, 30, 7)

# Télécharger données (sans interval)
try:
    data = cg.get_coin_market_chart_by_id(id=crypto, vs_currency="usd", days=jours)
    prix = [p[1] for p in data["prices"]]
    temps = pd.to_datetime([p[0] for p in data["prices"]], unit="ms")

    df = pd.DataFrame({"Date": temps, "Prix": prix})
    df.set_index("Date", inplace=True)

    st.line_chart(df["Prix"])

    # RSI simple
    delta = df["Prix"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))

    st.subheader("RSI (14)")
    st.line_chart(RSI)

    # Signal simple
    dernier_RSI = RSI.iloc[-1]
    if dernier_RSI > 70:
        st.error("⚠️ Surachat → Signal de Vente")
    elif dernier_RSI < 30:
        st.success("✅ Survente → Signal d'Achat")
    else:
        st.info("⏸ Attente → Pas de signal clair")

except Exception as e:
    st.error(f"Erreur : {e}")