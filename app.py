import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
from alpha_vantage.foreignexchange import ForeignExchange

# =====================
# CONFIG
# =====================
API_KEY = "F91C9ZG3PRF68UUV"  # Clé Alpha Vantage
binance_client = Client()  
fx = ForeignExchange(key=API_KEY)

# =====================
# INTERFACE STREAMLIT
# =====================
st.title("📊 Quotex Style - Crypto & Forex")

mode = st.selectbox("Choisissez le marché :", ["Crypto", "Forex"])

if mode == "Crypto":
    crypto = st.selectbox("Choisissez une crypto :", ["BTCUSDT", "ETHUSDT", "BNBUSDT"])

    # Récupérer prix actuel Binance
    ticker = binance_client.get_symbol_ticker(symbol=crypto)
    price = float(ticker["price"])
    st.success(f"💰 Prix actuel de {crypto} : {price:.2f} USDT")

    # Données bougies
    klines = binance_client.get_klines(symbol=crypto, interval=Client.KLINE_INTERVAL_1MINUTE, limit=30)
    df = pd.DataFrame(klines, columns=["time","o","h","l","c","v","close_time","q","n","tb","tq","ignore"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["c"] = df["c"].astype(float)

    # Graphique
    fig, ax = plt.subplots()
    ax.plot(df["time"], df["c"], label="Prix")
    ax.set_title(f"Évolution de {crypto}")
    ax.legend()
    st.pyplot(fig)

elif mode == "Forex":
    pair = st.selectbox("Choisissez une paire Forex :", ["EUR/USD", "GBP/USD", "USD/JPY"])

    # Récupérer données Alpha Vantage
    from_symbol, to_symbol = pair.split("/")
    data, _ = fx.get_currency_exchange_intraday(
        from_symbol=from_symbol, 
        to_symbol=to_symbol, 
        interval="1min", 
        outputsize="compact"
    )

    df = pd.DataFrame.from_dict(data, orient="index")
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close"
    })
    df.index = pd.to_datetime(df.index)
    df = df.astype(float).sort_index()

    st.success(f"💰 Dernier prix {pair} : {df['close'].iloc[-1]:.5f}")

    # Graphique
    fig, ax = plt.subplots()
    ax.plot(df.index, df["close"], label="Prix Forex")
    ax.set_title(f"Évolution de {pair}")
    ax.legend()
    st.pyplot(fig)