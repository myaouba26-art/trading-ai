import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================
# Configuration
# ============================
st.set_page_config(page_title="Trading App", layout="wide")

API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

st.title("📊 Application de Trading (RSI + EMA)")

# Choix de la paire
symbol = st.text_input("Entrez le symbole (ex: BTCUSD, EURUSD, AAPL)", "BTCUSD")
market_type = st.selectbox("Type de marché", ["crypto", "forex", "equity"])
interval = st.selectbox("Intervalle", ["1min", "5min", "15min", "30min", "60min"])

# ============================
# Récupération des données
# ============================
def get_data(symbol, market_type, interval):
    if market_type == "crypto":
        function = "CRYPTO_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&market=USD&interval={interval}&apikey={API_KEY}"
        key = f"Time Series Crypto ({interval})"
    elif market_type == "forex":
        function = "FX_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&interval={interval}&apikey={API_KEY}"
        key = f"Time Series FX ({interval})"
    else:  # equity
        function = "TIME_SERIES_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={API_KEY}"
        key = f"Time Series ({interval})"

    r = requests.get(url)
    data = r.json()

    if key not in data:
        st.error("Impossible de récupérer les données. Vérifie ton symbole ou limite API.")
        return None

    df = pd.DataFrame(data[key]).T
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

df = get_data(symbol, market_type, interval)

if df is not None:
    # ============================
    # Indicateurs techniques
    # ============================
    # RSI
    delta = df['4. close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # EMA
    df['EMA_20'] = df['4. close'].ewm(span=20, adjust=False).mean()

    # ============================
    # Signaux
    # ============================
    last_rsi = df['RSI'].iloc[-1]
    last_price = df['4. close'].iloc[-1]
    last_ema = df['EMA_20'].iloc[-1]

    if last_rsi < 30 and last_price > last_ema:
        signal = "Acheter ✅"
    elif last_rsi > 70 and last_price < last_ema:
        signal = "Vendre ❌"
    else:
        signal = "Attendre ⏳"

    st.subheader(f"Signal actuel : {signal}")
    st.write(f"RSI = {last_rsi:.2f} | Prix = {last_price:.2f} | EMA20 = {last_ema:.2f}")

    # ============================
    # Graphique en chandeliers
    # ============================
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['1. open'],
        high=df['2. high'],
        low=df['3. low'],
        close=df['4. close'],
        name="Bougies"
    )])

    # Ajouter EMA
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['EMA_20'],
        line=dict(color='blue', width=1.5),
        name="EMA 20"
    ))

    fig.update_layout(
        title=f"Graphique {symbol} ({interval})",
        xaxis_title="Date",
        yaxis_title="Prix",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)