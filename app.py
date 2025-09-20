import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import ta

# Fonction pour récupérer les prix depuis CoinGecko
def get_price_history(crypto="bitcoin", vs_currency="usd", days=1, interval="minute"):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
    params = {"vs_currency": vs_currency, "days": days, "interval": interval}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    else:
        return None

# Interface Streamlit
st.title("📊 Crypto Trading avec RSI + EMA + Probabilité")

crypto = st.selectbox("Choisissez une crypto :", ["bitcoin", "ethereum", "cardano", "solana"])
vs_currency = st.selectbox("Devise :", ["usd", "eur"])

if st.button("Obtenir les données"):
    df = get_price_history(crypto, vs_currency, days=1, interval="minute")

    if df is not None:
        # Calcul RSI et EMA
        df["RSI"] = ta.momentum.RSIIndicator(df["price"], window=14).rsi()
        df["EMA20"] = ta.trend.EMAIndicator(df["price"], window=20).ema_indicator()

        # Derniers indicateurs
        last_price = df["price"].iloc[-1]
        last_rsi = df["RSI"].iloc[-1]
        last_ema = df["EMA20"].iloc[-1]

        # Déterminer le signal et la probabilité
        if last_rsi < 30 and last_price > last_ema:
            signal = "📈 Achat fort"
            prob = 85
        elif last_rsi > 70 and last_price < last_ema:
            signal = "📉 Vente forte"
            prob = 85
        elif last_rsi < 30:
            signal = "🟢 Achat"
            prob = 60
        elif last_rsi > 70:
            signal = "🔴 Vente"
            prob = 60
        else:
            signal = "🤝 Attente"
            prob = 40

        # Afficher résultats
        st.success(f"💰 Prix actuel de {crypto.capitalize()} : {last_price:.2f} {vs_currency.upper()}")
        st.info(f"📊 RSI actuel : {last_rsi:.2f}")
        st.info(f"📉 EMA20 : {last_ema:.2f}")
        st.warning(f"Signal : {signal} ({prob} % de probabilité)")

        # Graphique Prix + EMA
        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax1.set_title(f"Évolution de {crypto.capitalize()} avec EMA20")
        ax1.plot(df["timestamp"], df["price"], label="Prix", color="blue")
        ax1.plot(df["timestamp"], df["EMA20"], label="EMA20", color="orange")
        ax1.set_ylabel(f"Prix ({vs_currency.upper()})")
        ax1.legend(loc="upper left")
        st.pyplot(fig)

        # Graphique RSI
        fig2, ax2 = plt.subplots(figsize=(10, 3))
        ax2.plot(df["timestamp"], df["RSI"], label="RSI", color="red")
        ax2.axhline(70, color="gray", linestyle="--")
        ax2.axhline(30, color="gray", linestyle="--")
        ax2.set_title("RSI (14 périodes)")
        ax2.set_ylabel("RSI")
        ax2.legend()
        st.pyplot(fig2)

    else:
        st.error("🚨 Erreur de connexion à CoinGecko")