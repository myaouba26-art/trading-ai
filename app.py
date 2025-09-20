import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from alpha_vantage.foreignexchange import ForeignExchange

# =====================
# CONFIG
# =====================
API_KEY = "F91C9ZG3PRF68UUV"  # ta clé Alpha Vantage
fx = ForeignExchange(key=API_KEY)

# =====================
# INTERFACE
# =====================
st.title("📊 Quotex Style - Crypto & Forex")

mode = st.selectbox("Choisissez le marché :", ["Crypto", "Forex"])

# ===== CRYPTO =====
if mode == "Crypto":
    crypto = st.selectbox("Choisissez une crypto :", ["BTC-USD", "ETH-USD", "BNB-USD"])

    data = yf.download(crypto, period="1d", interval="1m")
    if not data.empty:
        last_price = data["Close"].iloc[-1]
        st.success(f"💰 Prix actuel de {crypto} : {last_price:.2f} USD")

        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"], label="Prix")
        ax.set_title(f"Évolution de {crypto}")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Impossible de récupérer les données crypto.")

# ===== FOREX =====
elif mode == "Forex":
    pair = st.selectbox("Choisissez une paire Forex :", ["EUR/USD", "GBP/USD", "USD/JPY"])
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

    fig, ax = plt.subplots()
    ax.plot(df.index, df["close"], label="Prix Forex")
    ax.set_title(f"Évolution de {pair}")
    ax.legend()
    st.pyplot(fig)