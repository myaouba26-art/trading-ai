import streamlit as st
import pandas as pd
import numpy as np

# Titre
st.title("Application de Trading IA")

# Simulation de données de prix
np.random.seed(42)
prix = np.cumsum(np.random.randn(100)) + 100  # Série fictive de prix
df = pd.DataFrame(prix, columns=["Prix"])

# Calcul RSI
delta = df["Prix"].diff()
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
perte = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / perte
df["RSI"] = 100 - (100 / (1 + rs))

# Calcul EMA
df["EMA"] = df["Prix"].ewm(span=20, adjust=False).mean()

# Score fondamental fictif (0 à 100)
score_fondamental = np.random.randint(40, 90)

# Signal de trading
signal = "Attendre"
if df["RSI"].iloc[-1] < 30 and score_fondamental > 60:
    signal = "Acheter ✅"
elif df["RSI"].iloc[-1] > 70 and score_fondamental < 50:
    signal = "Vendre ❌"

# Affichage
st.line_chart(df[["Prix", "EMA"]])
st.write("RSI actuel :", round(df["RSI"].iloc[-1], 2))
st.write("Score fondamental :", score_fondamental)
st.subheader(f"Signal de trading : {signal}")
