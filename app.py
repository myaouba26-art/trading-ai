import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

# 📌 Fonction avec cache pour limiter les appels API
@st.cache_data(ttl=300)  # garde les données en cache 5 minutes (300 sec)
def get_alpha_vantage_data(market, symbol, interval):
    if market == "Crypto":
        function = "CRYPTO_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&market=USD&interval={interval}&apikey={API_KEY}"
    elif market == "Forex":
        function = "FX_INTRADAY"
        from_symbol, to_symbol = symbol.split("/")
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={API_KEY}"
    else:
        function = "TIME_SERIES_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={API_KEY}"
    
    r = requests.get(url)
    data = r.json()

    # Vérifier erreurs API
    if "Error Message" in data or "Note" in data:
        return None
    
    # Récupérer les données
    key = [k for k in data.keys() if "Time Series" in k][0]
    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

# --- Interface ---
st.title("📊 Alpha Vantage (avec cache)")

market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])
symbol = st.text_input("Entrez la paire ou l’action :", "BTC/USD" if market=="Crypto" else "EUR/USD")
interval = st.selectbox("Intervalle :", ["1min", "5min", "15min", "30min", "60min"])

if st.button("Obtenir les données"):
    df = get_alpha_vantage_data(market, symbol, interval)
    if df is not None:
        st.success("✅ Données récupérées (stockées en cache 5 min)")
        st.line_chart(df["4. close"])
    else:
        st.error("⚠️ Erreur de connexion ou quota dépassé")