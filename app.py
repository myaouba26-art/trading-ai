import streamlit as st
import pandas as pd
import requests

# ----------------------------
# Fonction pour Alpha Vantage
# ----------------------------
def get_alpha_vantage_data(market, pair, interval):
    api_key = st.secrets["ALPHAVANTAGE_API_KEY"]

    # Nettoyer la paire (BTC/USD -> BTCUSD)
    pair_clean = pair.replace("/", "").upper()

    # Choisir le bon endpoint selon le marché
    if market == "Crypto":
        function = "CRYPTO_INTRADAY"
        symbol = pair_clean
        market_param = "USD"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&market={market_param}&interval={interval}&apikey={api_key}"

    elif market == "Forex":
        function = "FX_INTRADAY"
        from_symbol, to_symbol = pair.upper().split("/")
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={api_key}"

    elif market == "Actions":
        function = "TIME_SERIES_INTRADAY"
        symbol = pair_clean
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}"

    else:
        st.error("❌ Marché non reconnu")
        return None

    # Requête
    response = requests.get(url)
    data = response.json()

    # Vérifier si les données existent
    if "Time Series" not in str(data):
        st.warning("⚠️ Pas de données disponibles pour cette combinaison.")
        return None

    # Trouver la clé correcte
    for key in data.keys():
        if "Time Series" in key:
            ts_key = key
            break

    df = pd.DataFrame(data[ts_key]).T
    df = df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    })
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)

    return df


# ----------------------------
# Interface Streamlit
# ----------------------------
st.title("(Crypto / Forex / Actions)")

# Sélecteurs utilisateur
market = st.selectbox("Choisissez le marché :", ["Crypto", "Forex", "Actions"])
pair = st.text_input("Entrez la paire ou l’action :", "BTC/USD")
interval = st.selectbox("Intervalle :", ["1min", "5min", "15min", "30min", "60min"])

if st.button("Obtenir les données"):
    df = get_alpha_vantage_data(market, pair, interval)

    if df is not None:
        st.success("✅ Données récupérées avec succès !")
        st.write(df.head())  # affichage brut
        st.line_chart(df["Close"])  # graphique simple