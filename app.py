import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np

st.title("Application de Trading IA (Données Réelles)")

# Sélection de l’actif
ticker = st.text_input("Entrez le symbole (ex: BTC-USD, ETH-USD, AAPL, EURUSD=X)", "BTC-USD")

# Téléchargement des données (1 jour, 1m)
data = yf.download(ticker, period="1d", interval="1m")

if not data.empty:
    # Calcul RSI
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    perte = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / perte
    data["RSI"] = 100 - (100 / (1 + rs))

    # Calcul EMA
    data["EMA"] = data["Close"].ewm(span=20, adjust=False).mean()

    # Score fondamental fictif
    score_fondamental = np.random.randint(40, 90)

    # Signal de trading
    signal = "Attendre"
    if data["RSI"].iloc[-1] < 30 and score_fondamental > 60:
        signal = "Acheter ✅"
    elif data["RSI"].iloc[-1] > 70 and score_fondamental < 50:
        signal = "Vendre ❌"

    # Affichage graphique
    st.line_chart(data[["Close", "EMA"]])

    # Indicateurs
    st.write("RSI actuel :", round(data["RSI"].iloc[-1], 2))
    st.write("Score fondamental :", score_fondamental)
    st.subheader(f"Signal de trading : {signal}")

else:
    st.error("Impossible de récupérer les données. Vérifiez le symbole.")
