import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.title("Mon Application de Trading IA (Données Réelles)")

# Entrées utilisateur
symbol = st.text_input("Symbole (ex: BTC-USD, ETH-USD, AAPL, EURUSD=X)", "ETH-USD")
interval = st.selectbox("Intervalle", ["1m","5m","15m","30m","1h","1d"])
period = st.selectbox("Période", ["1d","5d","7d","1mo","3mo","6mo","1y"])

st.write(f"Téléchargement de {symbol} — interval: {interval} — period: {period}")

try:
    data = yf.download(tickers=symbol, interval=interval, period=period)
    if data.empty:
        st.error("⚠️ Pas de données disponibles pour ce symbole / intervalle / période.")
    else:
        st.line_chart(data["Close"])

        # === Calcul RSI ===
        delta = data["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data["RSI"] = rsi

        # === Calcul EMA (20) ===
        data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()

        # Score fondamental fictif (aléatoire)
        fundamental_score = np.random.randint(40, 90)
        st.metric("Score fondamental (fictif)", fundamental_score)

        # Affichage
        st.line_chart(data[["Close","EMA20"]])
        st.line_chart(data["RSI"])

except Exception as e:
    st.error(f"Erreur lors du téléchargement : {e}")
