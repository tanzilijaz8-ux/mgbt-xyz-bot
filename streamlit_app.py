import streamlit as st
import pandas as pd
from strategy import generate_signals

st.set_page_config(page_title="MGBT XYZ Bot", layout="wide")

st.title("📈 MGBT XYZ Bot")
st.write("✅ Streamlit app connected with `strategy.py`")

# --- Fake test data ---
test_data = pd.DataFrame({
    "sma_fast": [105, 98, 110],
    "sma_slow": [100, 100, 108],
    "rsi": [65, 40, 80],
    "macd": [1.2, -0.5, 0.3],
    "macd_signal": [1.0, -0.2, 0.5],
    "macd_diff": [0.2, -0.3, -0.2]
})

# --- Generate signals using your strategy ---
result = generate_signals(test_data)

st.subheader("📊 Trading Signals")
st.dataframe(result)


