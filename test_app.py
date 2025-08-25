import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MGBT XYZ Bot", layout="wide")

st.title("✅ App loaded successfully")
st.write("If you can see this, Streamlit is rendering properly.")

# --- Strategy functions ---
def rule_based_signal(row):
    sma_fast = float(row["sma_fast"])
    sma_slow = float(row["sma_slow"])
    rsi = float(row["rsi"])
    macd = float(row["macd"])
    macd_signal = float(row["macd_signal"])

    if sma_fast > sma_slow and rsi < 70 and macd > macd_signal:
        return 1
    elif sma_fast < sma_slow and rsi > 30 and macd < macd_signal:
        return -1
    else:
        return 0

def generate_signals(df, use_ml=False, model_bundle=None):
    if use_ml and model_bundle:
        features = df[["rsi", "sma_fast", "sma_slow", "macd", "macd_signal", "macd_diff"]]
        df["signal"] = model_bundle["model"].predict(features)
    else:
        df["signal"] = df.apply(rule_based_signal, axis=1)
    return df

# --- Test with fake data ---
st.subheader("📊 Test Signals Output")

test_data = pd.DataFrame({
    "sma_fast": [105, 98, 110],
    "sma_slow": [100, 100, 108],
    "rsi": [65, 40, 80],
    "macd": [1.2, -0.5, 0.3],
    "macd_signal": [1.0, -0.2, 0.5],
    "macd_diff": [0.2, -0.3, -0.2]
})

result = generate_signals(test_data)
st.dataframe(result)
