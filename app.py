import streamlit as st
import pandas as pd
import numpy as np
from binance.client import Client

# Initialisation du client Binance (clé API pas obligatoire pour les données publiques)
client = Client()

# Titre de l'application
st.title("📊 Application de Trading IA (Données Binance)")

# Choix de la crypto et des paramètres
symbol = st.text_input("Symbole (ex: BTCUSDT, ETHUSDT, BNBUSDT)", "ETHUSDT")
interval = st.selectbox("Intervalle", ["1m","5m","15m","30m","1h","1d"])
limit = st.slider("Nombre de bougies à récupérer", 50, 500, 100)

st.write(f"Téléchargement de {symbol} — intervalle: {interval} — {limit} bougies")

try:
    # Récupération des bougies depuis Binance
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    # Conversion en DataFrame
    df = pd.DataFrame(klines, columns=[
        "Open time","Open","High","Low","Close","Volume",
        "Close time","Quote asset volume","Number of trades",
        "Taker buy base","Taker buy quote","Ignore"
    ])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])

    # Calcul RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi

    # Calcul EMA 20
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # Score fondamental fictif
    fundamental_score = np.random.randint(40, 90)

    # 📈 Affichage des graphiques
    st.subheader("Cours et EMA20")
    st.line_chart(df[["Close","EMA20"]])

    st.subheader("RSI")
    st.line_chart(df["RSI"])

    # 📊 Indicateur fondamental fictif
    st.metric("Score fondamental (fictif)", fundamental_score)

except Exception as e:
    st.error(f"❌ Erreur lors du téléchargement des données : {e}")