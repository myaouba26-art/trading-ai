import requests
import pandas as pd
import streamlit as st

def get_alpha_vantage_data(market, pair, interval):
    api_key = st.secrets["ALPHAVANTAGE_API_KEY"]

    # Nettoyer la paire (BTC/USD -> BTCUSD)
    pair_clean = pair.replace("/", "").upper()

    # Choisir le bon endpoint selon le marché
    if market == "Crypto":
        function = "CRYPTO_INTRADAY"
        symbol = pair_clean
        market_param = "USD"  # par défaut en dollars
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&market={market_param}&interval={interval}&apikey={api_key}"

    elif market == "Forex":
        function = "FX_INTRADAY"
        # Exemple EUR/USD -> from_symbol=EUR, to_symbol=USD
        from_symbol, to_symbol = pair.upper().split("/")
        url = f"https://www.alphavantage.co/query?function={function}&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={api_key}"

    elif market == "Actions":
        function = "TIME_SERIES_INTRADAY"
        symbol = pair_clean
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}"

    else:
        st.error("❌ Marché non reconnu")
        return None

    # Récupérer les données
    response = requests.get(url)
    data = response.json()

    # Vérifier si les données existent
    if "Time Series" not in str(data):
        st.warning("⚠️ Pas de données disponibles pour cette combinaison.")
        return None

    # Trouver la bonne clé (varie selon fonction)
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