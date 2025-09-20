import streamlit as st
from pycoingecko import CoinGeckoAPI
import time
import pandas as pd
import matplotlib.pyplot as plt

cg = CoinGeckoAPI()

st.title("📊 Prix en temps réel (CoinGecko API)")

cryptos = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin"
}

crypto = st.selectbox("Choisissez une crypto :", list(cryptos.keys()))

auto_update = st.checkbox("🔄 Mise à jour automatique (toutes les 5 secondes)")

price_placeholder = st.empty()
chart_placeholder = st.empty()

prices = []
timestamps = []

def get_price(crypto_id):
    try:
        data = cg.get_price(ids=crypto_id, vs_currencies="usd")
        return data[crypto_id]["usd"]
    except:
        return None

if st.button("Obtenir le prix") or auto_update:
    while True:
        price = get_price(cryptos[crypto])
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
            price_placeholder.error("⚠️ Erreur de connexion CoinGecko")

        if not auto_update:
            break
        time.sleep(5)