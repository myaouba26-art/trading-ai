import streamlit as st
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.title("📊 Crypto Trading avec RSI + EMA + Probabilité")

# Sélection crypto et devise
crypto = st.selectbox("Choisissez une crypto :", ["bitcoin", "ethereum", "solana"])
devise = st.selectbox("Devise :", ["usd", "eur", "usdt"])

if st.button("Obtenir les données"):
    try:
        # ✅ On récupère uniquement le prix actuel
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto, "vs_currencies": devise}
        response = requests.get(url, params=params)
        data = response.json()

        if crypto in data:
            prix = data[crypto][devise]
            st.success(f"💰 Prix actuel de {crypto.capitalize()} : {prix} {devise.upper()}")

            # 🔹 Simuler un petit historique (pour RSI & EMA provisoires)
            dates = [datetime.datetime.now() - datetime.timedelta(minutes=i) for i in range(30)]
            prix_fake = [prix * (1 + (0.01 * (i % 5 - 2))) for i in range(30)]  # petites variations simulées

            df = pd.DataFrame({"date": dates[::-1], "prix": prix_fake[::-1]})

            # Calcul RSI (simplifié)
            delta = df["prix"].diff()
            gain = delta.clip(lower=0).mean()
            loss = -delta.clip(upper=0).mean()
            rs = gain / loss if loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))

            # Calcul EMA
            ema = df["prix"].ewm(span=14, adjust=False).mean()

            # Afficher graphiques
            st.line_chart(df.set_index("date")["prix"])
            st.line_chart(ema)

            # Probabilité fictive basée sur RSI
            if rsi > 70:
                decision = "📉 Surachat → Probabilité forte de baisse"
            elif rsi < 30:
                decision = "📈 Survente → Probabilité forte de hausse"
            else:
                decision = "⏸ Attente → Marché neutre"

            st.info(f"RSI actuel : {rsi:.2f} → {decision}")

        else:
            st.error("❌ Erreur : Crypto non trouvée dans CoinGecko")

    except Exception as e:
        st.error(f"🚨 Erreur de connexion à CoinGecko : {e}")