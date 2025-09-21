import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================
# Configuration
# ============================
st.set_page_config(page_title="Trading App", layout="wide")
st.title("📊 Application de Trading (RSI + EMA)")

API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

# ============================
# Fonction de récupération avec cache
# ============================
@st.cache_data(ttl=60)  # garde les données en cache 60 sec
def get_data(symbol, market_type, interval):
    base_url = "https://www.alphavantage.co/query"

    if market_type == "crypto":
        function = "CRYPTO_INTRADAY"
        from_symbol, to_symbol = symbol[:3], symbol[3:]
        params = {
            "function": function,
            "symbol": from_symbol,
            "market": to_symbol,
            "interval": interval,
            "apikey": API_KEY
        }
    elif market_type == "forex":
        function = "FX_INTRADAY"
        from_symbol, to_symbol = symbol[:3], symbol[3:]
        params = {
            "function": function,
            "from_symbol": from_symbol,
            "to_symbol": to_symbol,
            "interval": interval,
            "apikey": API_KEY
        }
    else:  # equity
        function = "TIME_SERIES_INTRADAY"
        params = {
            "function": function,
            "symbol": symbol,
            "interval": interval,
            "apikey": API_KEY
        }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        key = [k for k in data.keys() if "Time Series" in k][0]
        df = pd.DataFrame(data[key]).T
        df = df.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        })
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)

        return df.sort_index()

    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# ============================
# Sélection utilisateur
# ============================
symbol = st.text_input("Entrez un symbole :", "BTCUSD")
market_type = st.selectbox("Type de marché :", ["crypto", "forex", "equity"])
interval = st.selectbox("Intervalle :", ["1min", "5min", "15min", "30min", "60min"])

df = get_data(symbol, market_type, interval)

# ============================
# Analyse et indicateurs
# ============================
if df is not None:
    # RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # EMA
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # Dernières valeurs
    last_rsi = df["RSI"].iloc[-1]
    last_price = df["close"].iloc[-1]
    last_ema = df["EMA_20"].iloc[-1]

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
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Bougies"
    )])

    # Ajouter EMA
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["EMA_20"],
        line=dict(color="blue", width=1.5),
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
else:
    st.warning("⚠️ Pas de données disponibles pour ce symbole ou intervalle.")