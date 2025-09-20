import streamlit as st
import requests
import time

st.title("📈 Prix en temps réel (CoinCap API)")

# Entrée utilisateur
symbol = st.text_input("Entrez le symbole (ex: bitcoin, ethereum, cardano)", "bitcoin").lower()

# Fonction pour récupérer le prix depuis CoinCap
def get_coincap_price(symbol):
    url = f"https://api.coincap.io/v2/assets/{symbol}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["priceUsd"]
        else:
            return None
    except:
        return None

# Bouton pour obtenir le prix
if st.button("Obtenir le prix"):
    price = get_coincap_price(symbol)
    if price:
        st.success(f"💰 Prix actuel de {symbol.upper()} : {float(price):.2f} USD")
    else:
        st.error("⚠️ Impossible de récupérer les données CoinCap")

# Mise à jour automatique toutes les 5 secondes
st.write("🔄 Mise à jour automatique (toutes les 5 secondes)")
placeholder = st.empty()

for i in range(5):  # rafraîchit 5 fois (soit 25 secondes)
    price = get_coincap_price(symbol)
    if price:
        placeholder.metric(label=f"Prix {symbol.upper()}", value=f"{float(price):.2f} USD")
    else:
        placeholder.error("⚠️ Erreur de connexion à CoinCap")
    time.sleep(5)