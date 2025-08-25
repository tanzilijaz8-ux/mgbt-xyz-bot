import streamlit as st
import pandas as pd
from strategy import generate_signals

st.set_page_config(page_title="MGBT XYZ Bot", layout="wide")

st.title("📊 MGBT XYZ Bot - Signal Generator")

# --- Trading Platform ---
st.subheader("Trading Platform")
platform = st.radio("Select Platform", ["Quotex", "Pocket Option", "Olymp Trade", "IQ Option"], horizontal=True)

# --- Market Type ---
st.subheader("Market Type")
market_type = st.radio("Choose Market Type", ["LIVE", "OTC"], horizontal=True)

# --- Currency Pair ---
st.subheader("Currency Pair")
currency_pair = st.selectbox("Select Pair", ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"])
if market_type == "OTC":
    currency_pair += " OTC"

# --- Time Frame ---
st.subheader("Time Frame")
time_frame = st.radio(
    "Select Time Frame",
    ["5s", "10s", "15s", "30s", "1m", "5m", "10m", "15m", "30m"],
    horizontal=True
)

# --- Fake / Demo Data ---
sample_data = pd.DataFrame({
    "sma_fast": [105, 110, 95],
    "sma_slow": [100, 108, 97],
    "rsi": [40, 65, 80],
    "macd": [0.5, -0.3, 0.2],
    "macd_signal": [0.3, -0.2, 0.25],
    "macd_diff": [0.2, -0.1, -0.05]
})

signals = generate_signals(sample_data)

# --- Show Result ---
st.subheader("📌 Generated Signal")
last_signal = signals["signal"].iloc[-1]

if last_signal == 1:
    st.success(f"✅ BUY Signal for {currency_pair} ({time_frame}) on {platform}")
elif last_signal == -1:
    st.error(f"❌ SELL Signal for {currency_pair} ({time_frame}) on {platform}")
else:
    st.warning(f"⏸ HOLD Signal for {currency_pair} ({time_frame}) on {platform}")

# Show table
with st.expander("🔍 View Signal Data"):
    st.dataframe(signals)
