import streamlit as st
import requests
import pandas as pd

API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

@st.cache_data(ttl=300)
def get_alpha_vantage_data(market, symbol, interval):
    if market == "Crypto":
        function = "CRYPTO_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&market=USD&interval={interval}&apikey={API_KEY}"
    elif market == "Forex":
        function = "FX_INTRADAY"
        from_symbol, to_symbol = symbol.split("/")
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={API_KEY}"
    else:
        function = "TIME_SERIES_INTRADAY"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={API_KEY}"
    
    r = requests.get(url)
    data = r.json()

    # Vérifier si Alpha Vantage renvoie une erreur ou un quota dépassé
    if "Error Message" in data:
        return None, "❌ Erreur dans la requête (mauvais symbole ou fonction)."
    if "Note" in data:
        return None, "⚠️ Quota dépassé (attendez 1 minute)."

    # Trouver la clé "Time Series"
    time_series_keys = [k for k in data.keys() if "Time Series" in k]
    if not time_series_keys:
        return None, "⚠️ Pas de données disponibles pour cette combinaison."

    key = time_series_keys[0]
    df = pd.DataFrame.from_dict(data[key], orient="index")
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df.sort_index(), None

# --- Interface ---
st.title("📊 Alpha Vantage (avec cache et gestion des erreurs)")

market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])
symbol = st.text_input("Entrez la paire ou l’action :", "BTC/USD" if market=="Crypto" else "EUR/USD")
interval = st.selectbox("Intervalle :", ["1min", "5min", "15min", "30min", "60min"])

if st.button("Obtenir les données"):
    df, error = get_alpha_vantage_data(market, symbol, interval)
    if error:
        st.error(error)
    elif df is not None:
        st.success("✅ Données récupérées")
        st.line_chart(df["4. close"])