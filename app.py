import streamlit as st
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Prix en temps réel avec graphique (Binance API)")

cryptos = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "XRPUSDT", "LTCUSDT"]
crypto = st.selectbox("Choisissez une crypto :", cryptos)

auto_update = st.checkbox("🔄 Mise à jour automatique (toutes les 5 secondes)")

price_placeholder = st.empty()
chart_placeholder = st.empty()

prices = []
timestamps = []

def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        else:
            return None
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
            ax.plot(df["Temps"], df["Prix"], marker="o", linestyle="-", color="blue")
            ax.set_xlabel("Temps")
            ax.set_ylabel("Prix en USD")
            ax.set_title(f"Évolution en temps réel de {crypto}")
            plt.xticks(rotation=45)
            chart_placeholder.pyplot(fig)

        else:
            price_placeholder.error("⚠️ Erreur de connexion à Binance")

        if not auto_update:
            break
        time.sleep(5)