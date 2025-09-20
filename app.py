import streamlit as st
from binance.client import Client
import pandas as pd
import time

# ----------------------------
# Binance client (API publique → pas besoin de clé pour juste les prix)
# ----------------------------
client = Client()

st.title("📈 Suivi en temps réel (Binance)")

# Sélection de la paire
symbol = st.text_input("Entre le symbole (ex: BTCUSDT, ETHUSDT)", "BTCUSDT")

# Bouton pour lancer
if st.button("Obtenir le prix"):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        st.success(f"💰 Prix actuel de {symbol} : {ticker['price']} USDT")
    except Exception as e:
        st.error(f"Erreur : {e}")

# Mise à jour automatique toutes les 5 secondes
st.write("🔄 Mise à jour automatique (toutes les 5 secondes)")
placeholder = st.empty()

for i in range(10):  # rafraîchit 10 fois
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        placeholder.metric(label=f"Prix {symbol}", value=f"{ticker['price']} USDT")
    except:
        placeholder.error("Erreur de connexion à Binance")
    time.sleep(5)