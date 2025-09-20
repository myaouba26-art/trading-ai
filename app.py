import streamlit as st
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Prix en temps réel avec graphique (CoinCap API)")

# Liste des cryptos disponibles
cryptos = ["bitcoin", "ethereum", "cardano", "dogecoin", "solana", "xrp", "litecoin"]

# Sélecteur
crypto = st.selectbox("Choisissez une crypto :", cryptos)

# Checkbox pour activer la mise à jour automatique
auto_update = st.checkbox("🔄 Mise à jour automatique (toutes les 5 secondes)")

# Zone d'affichage du prix
price_placeholder = st.empty()
chart_placeholder = st.empty()

# Historique des prix
prices = []
timestamps = []

def get_price(crypto):
    try:
        url = f"https://api.coincap.io/v2/assets/{crypto}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data["data"]["priceUsd"])
        else:
            return None
    except:
        return None

if st.button("Obtenir le prix") or auto_update:
    while True:
        price = get_price(crypto)
        if price:
            prices.append(price)
            timestamps.append(time.strftime("%H:%M:%S"))

            # Affichage prix
            price_placeholder.success(f"💰 Prix actuel de {crypto.capitalize()} : {price:.2f} USD")

            # Affichage graphique
            df = pd.DataFrame({"Temps": timestamps, "Prix": prices})
            fig, ax = plt.subplots()
            ax.plot(df["Temps"], df["Prix"], marker="o", linestyle="-", color="blue")
            ax.set_xlabel("Temps")
            ax.set_ylabel("Prix en USD")
            ax.set_title(f"Évolution en temps réel de {crypto.capitalize()}")
            plt.xticks(rotation=45)
            chart_placeholder.pyplot(fig)

        else:
            price_placeholder.error("⚠️ Erreur de connexion à CoinCap")

        if not auto_update:
            break  # Sortir si pas d'auto-update
        time.sleep(5)  # Attente avant nouvelle mise à jour