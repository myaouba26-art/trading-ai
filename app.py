import streamlit as st
import requests
import pandas as pd
import time

# récupérer la clé depuis les secrets Streamlit
API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

st.title("📊 Cours en temps réel avec Alpha Vantage")

# Choix du marché
market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])

if market == "Crypto":
    symbol = st.text_input("Entrez une paire crypto (ex: BTC/USD)", "BTC/USD")
    interval = st.selectbox("Intervalle :", ["1min", "5min", "15min", "30min", "60min"])
    if st.button("Obtenir les données"):
        url = f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol.replace('/','')}&market=USD&interval={interval}&apikey={API_KEY}"
        r = requests.get(url)
        data = r.json()

        if "Time Series Crypto" in data:
            df = pd.DataFrame(data[f"Time Series Crypto ({interval})"]).T
            df = df.astype(float)
            st.line_chart(df["4. close"])
            st.success(f"Dernier prix de {symbol} : {df['4. close'].iloc[0]} USD")
        else:
            st.error("Erreur de connexion ou quota dépassé.")

elif market == "Forex":
    pair = st.text_input("Entrez une paire Forex (ex: EUR/USD)", "EUR/USD")
    if st.button("Obtenir les données"):
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={pair.split('/')[0]}&to_currency={pair.split('/')[1]}&apikey={API_KEY}"
        r = requests.get(url).json()
        if "Realtime Currency Exchange Rate" in r:
            rate = r["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
            st.success(f"Taux actuel {pair} : {rate}")
        else:
            st.error("Erreur API ou quota dépassé.")

elif market == "Actions":
    symbol = st.text_input("Entrez un ticker action (ex: AAPL, TSLA)", "AAPL")
    if st.button("Obtenir les données"):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
        r = requests.get(url).json()
        if "Time Series (5min)" in r:
            df = pd.DataFrame(r["Time Series (5min)"]).T
            df = df.astype(float)
            st.line_chart(df["4. close"])
            st.success(f"Dernier prix {symbol} : {df['4. close'].iloc[0]} USD")
        else:
            st.error("Erreur API ou quota dépassé.")