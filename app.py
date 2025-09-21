import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

# Récupération de la clé API depuis les secrets
API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

# Fonction pour récupérer les données
def get_alpha_vantage_data(market, symbol, interval):
    base_url = "https://www.alphavantage.co/query?"

    if market == "Crypto":
        function = "CRYPTO_INTRADAY"
        url = f"{base_url}function={function}&symbol={symbol}&market=USD&interval={interval}&apikey={API_KEY}"
        key = f"Time Series Crypto ({interval})"
    else:
        function = "TIME_SERIES_INTRADAY"
        url = f"{base_url}function={function}&symbol={symbol}&interval={interval}&apikey={API_KEY}"
        key = f"Time Series ({interval})"

    response = requests.get(url)
    data = response.json()

    if key not in data:
        return None

    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    return df

# --- Interface Streamlit ---
st.title("📊 Alpha Vantage (Crypto / Forex / Actions)")

market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])
symbol = st.text_input("Entrez la paire ou l’action :", "BTC/USD" if market == "Crypto" else "AAPL")

# Intervalles selon le marché choisi
if market == "Crypto":
    intervals = ["5min", "15min", "30min", "60min"]
else:
    intervals = ["1min", "5min", "15min", "30min", "60min"]

interval = st.selectbox("Intervalle :", intervals)

if st.button("Obtenir les données"):
    df = get_alpha_vantage_data(market, symbol, interval)

    if df is None or df.empty:
        st.warning("⚠️ Pas de données disponibles pour cette combinaison.")
    else:
        st.success(f"Données reçues pour {symbol} ({interval})")

        # Affichage du graphique en chandelier
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])
        fig.update_layout(title=f"Graphique {symbol} ({interval})", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)