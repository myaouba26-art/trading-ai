import streamlit as st
from binance.client import Client
import time
import pandas as pd
import matplotlib.pyplot as plt

# Client Binance en mode public (pas besoin de clés pour les prix spot)
client = Client()

st.title("📊 Prix en temps réel (Binance)")

cryptos = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOGEUSDT"]
crypto = st.selectbox("Choisissez une crypto :", cryptos)

auto_update = st.checkbox("🔄 Mise à jour automatique (toutes les 5 secondes)")

price_placeholder = st.empty()
chart_placeholder = st.empty()

prices = []
timestamps = []

def get_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        return None

if st.button("Obtenir le prix") or auto_update:
    while True:
        price = get_price(crypto)
        if price:
            prices.append(price)
            timestamps.append(time.strftime("%H:%M:%S"))

            price_placeholder.success(f"💰 Prix actuel de {crypto} : {price:.2f} USD")

            df = pd.DataFrame({"Temps": timestamps, "Prix": prices})
            fig, ax = plt.subplots()
            ax.plot(df["Temps"], df["Prix"], marker="o", color="blue")
            ax.set_xlabel("Temps")
            ax.set_ylabel("Prix en USD")
            ax.set_title(f"Évolution de {crypto}")
            plt.xticks(rotation=45)
            chart_placeholder.pyplot(fig)
        else:
            price_placeholder.error("⚠️ Erreur de connexion Binance (via SDK)")

        if not auto_update:
            break
        time.sleep(5)