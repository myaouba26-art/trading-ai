import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="Trading IA (Données réelles)", layout="wide")
st.title("Application de Trading IA (Données Réelles)")

ticker = st.text_input("Symbole (ex: BTC-USD, ETH-USD, AAPL, EURUSD=X)", "ETH-USD")
interval = st.selectbox("Intervalle", ["1m","2m","5m","15m","30m","60m","90m","1d"], index=2)

# mapping period adapté selon interval (Yahoo limite les intraday)
period_map = {
    "1m": "7d",
    "2m": "7d",
    "5m": "7d",
    "15m": "60d",
    "30m": "60d",
    "60m": "120d",
    "90m": "120d",
    "1d": "5y"
}
period = period_map.get(interval, "7d")

st.info(f"Téléchargement de {ticker} — interval: {interval} — period: {period}")

# Télécharge les données
try:
    data = yf.download(tickers=ticker, period=period, interval=interval, progress=False, threads=False)
except Exception as e:
    st.error("Erreur durant le téléchargement des données depuis Yahoo Finance.")
    st.write(e)
    st.stop()

if data is None or data.empty:
    st.error("Impossible de récupérer des données (DataFrame vide). Vérifie le symbole ou change l'intervalle.")
    st.stop()

if data.shape[0] < 20:
    st.warning("Pas assez de bougies pour calculer les indicateurs (moins de 20). Essaie un intervalle plus long.")
    st.dataframe(data.tail(10))
    st.stop()

# Fonction RSI robuste
def compute_rsi(close, period=14):
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(period).mean()
    roll_down = down.rolling(period).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculs
data["RSI"] = compute_rsi(data["Close"], 14)
data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()

# Vérifie que les indicateurs existent (pas NaN)
dernier = data.iloc[-1]
if pd.isna(dernier["RSI"]) or pd.isna(dernier["EMA20"]) or pd.isna(dernier["EMA50"]):
    st.warning("Les indicateurs ne sont pas encore prêts (NaN). Attends quelques bougies ou change d'intervalle.")
    st.dataframe(data.tail(10)[["Close","RSI","EMA20","EMA50"]])
    st.stop()

# Score fondamental fictif
score_fondamental = np.random.randint(40, 90)

# Signal
signal = "Attendre"
confiance = 50
if (dernier["RSI"] < 30) and (dernier["EMA20"] > dernier["EMA50"]) and (score_fondamental > 60):
    signal = "Acheter ✅"
    confiance = 70
elif (dernier["RSI"] > 70) and (dernier["EMA20"] < dernier["EMA50"]) and (score_fondamental < 50):
    signal = "Vendre ❌"
    confiance = 70

# Affichages
st.metric("Signal actuel", signal, f"{confiance}%")
st.write(f"RSI : {dernier['RSI']:.2f}    EMA20 : {dernier['EMA20']:.2f}    EMA50 : {dernier['EMA50']:.2f}")
st.write(f"Score fondamental (fictif) : {score_fondamental}")

chart_df = data[["Close","EMA20","EMA50"]].copy()
st.line_chart(chart_df)

st.subheader("Dernières lignes de données")
st.dataframe(data.tail(10)[["Close","RSI","EMA20","EMA50"]])
