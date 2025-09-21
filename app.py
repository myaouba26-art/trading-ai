import streamlit as st
import requests

# Récupérer ta clé API Alpha Vantage depuis les secrets
api_key = st.secrets["ALPHAVANTAGE_API_KEY"]

st.title("🔑 Test Alpha Vantage API")

# Paramètres de la requête
symbol = "BTC"
market = "USD"

url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency={market}&apikey={api_key}"

# Faire la requête
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if "Realtime Currency Exchange Rate" in data:
        prix = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        st.success(f"💰 Prix actuel du {symbol}/{market} : {prix}")
    else:
        st.error("Erreur : pas de données (limite atteinte ou mauvaise clé)")
else:
    st.error("Erreur de connexion à l’API Alpha Vantage")