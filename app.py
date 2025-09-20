import streamlit as st
import requests
import time

st.title("📈 Prix en temps réel (Binance API)")

# Input pour choisir la paire
symbol = st.text_input("Entrez le symbole (ex: BTCUSDT, ETHUSDT)", "BTCUSDT").upper()

# Fonction pour récupérer le prix
def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        data = response.json()
        return data["price"]
    except:
        return None

# Affichage du prix
if st.button("Obtenir le prix"):
    price = get_binance_price(symbol)
    if price:
        st.success(f"💰 Prix actuel de {symbol} : {price} USDT")
    else:
        st.error("Erreur lors de la récupération du prix")

# Mise à jour automatique toutes les 5 secondes
st.write("🔄 Mise à jour automatique (toutes les 5 secondes)")
placeholder = st.empty()

for i in range(10):  # rafraîchit 10 fois
    price = get_binance_price(symbol)
    if price:
        placeholder.metric(label=f"Prix {symbol}", value=f"{price} USDT")
    else:
        placeholder.error("Erreur de connexion à Binance")
    time.sleep(5)