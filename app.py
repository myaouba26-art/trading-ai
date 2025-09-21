import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("(Crypto / Forex / Actions) Trading App")

# === Choix du marché ===
market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])

# === Choix de la paire / action selon le marché ===
if market == "Crypto":
    pair = st.selectbox("Choisissez une paire Crypto :", [
        "BTC-USD",
        "ETH-USD",
        "LTC-USD",
        "ADA-USD",
        "BNB-USD",
        "XRP-USD",
        "SOL-USD",
        "DOGE-USD"
    ])

elif market == "Forex":
    pair = st.selectbox("Choisissez une paire Forex :", [
        "EURUSD=X",
        "GBPUSD=X",
        "USDJPY=X",
        "USDCHF=X",
        "AUDUSD=X",
        "NZDUSD=X",
        "USDCAD=X"
    ])

elif market == "Actions":
    pair = st.selectbox("Choisissez une action :", [
        "AAPL",   # Apple
        "TSLA",   # Tesla
        "MSFT",   # Microsoft
        "GOOGL",  # Alphabet
        "AMZN",   # Amazon
        "META",   # Meta (Facebook)
        "NVDA"    # Nvidia
    ])

# === Choix de l’intervalle ===
interval = st.selectbox("Intervalle :", ["1m", "5m", "15m", "30m", "1h", "1d"])

# === Bouton pour récupérer les données ===
if st.button("Obtenir les données"):
    try:
        df = yf.download(tickers=pair, period="1d", interval=interval)

        if df.empty:
            st.warning("⚠️ Pas de données disponibles pour cette combinaison.")
        else:
            st.success("✅ Données récupérées avec succès !")

            # === Affichage du graphique ===
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])

            fig.update_layout(title=f"Cours de {pair}", xaxis_title="Temps", yaxis_title="Prix")
            st.plotly_chart(fig)

            # === Calcul RSI (exemple simple) ===
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            df['RSI'] = rsi

            st.line_chart(df['RSI'])

    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des données : {e}")