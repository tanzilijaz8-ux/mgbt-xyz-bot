import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategy import generate_signals

# --- Page config ---
st.set_page_config(page_title="MGBT XYZ Bot", layout="wide")

# --- Header ---
st.title("🤖 MGBT XYZ Bot")
st.write("Your AI-powered trading signals dashboard.")

# --- Sidebar Controls ---
st.sidebar.header("Settings ⚙️")
stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
date_range = st.sidebar.date_input("Select Date Range")

# --- Dummy Data (replace later with live data e.g., yfinance) ---
data = {
    "sma_fast": [95, 105, 110],
    "sma_slow": [100, 100, 100],
    "rsi": [40, 65, 80],
    "macd": [-0.5, 1.2, 0.2],
    "macd_signal": [-0.2, 1.0, 0.5],
    "macd_diff": [0.3, 0.2, -0.3],
}
df = pd.DataFrame(data)

# --- Generate Signals ---
df = generate_signals(df)

# --- Display Signals ---
st.subheader("📊 Trading Signals")
st.dataframe(df, use_container_width=True)

# --- Plot (example RSI chart) ---
st.subheader("📈 RSI Chart")
fig, ax = plt.subplots()
ax.plot(df.index, df["rsi"], label="RSI", color="blue")
ax.axhline(70, color="red", linestyle="--", label="Overbought")
ax.axhline(30, color="green", linestyle="--", label="Oversold")
ax.set_title("RSI Indicator")
ax.legend()
st.pyplot(fig)

st.success("✅ Bot is running. Modify strategy.py to change rules.")
