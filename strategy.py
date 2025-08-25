import pandas as pd

# --- Rule-based trading signal function ---
def rule_based_signal(row: pd.Series) -> int:
    """
    Generate a trading signal based on SMA crossovers, RSI, and MACD.
    Returns:
        1 = Buy
       -1 = Sell
        0 = Hold
    """

    sma_fast = float(row["sma_fast"])
    sma_slow = float(row["sma_slow"])
    rsi = float(row["rsi"])
    macd = float(row["macd"])
    macd_signal = float(row["macd_signal"])

    # --- Example rules ---
    if sma_fast > sma_slow and rsi < 70 and macd > macd_signal:
        return 1   # ✅ Buy
    elif sma_fast < sma_slow and rsi > 30 and macd < macd_signal:
        return -1  # ❌ Sell
    else:
        return 0   # ⏸ Hold


# --- Apply strategy to entire DataFrame ---
def generate_signals(df: pd.DataFrame, use_ml: bool = False, model_bundle=None) -> pd.DataFrame:
    """
    Generate trading signals for the full dataset.
    If use_ml=True, predictions are made using a trained ML model.
    """

    if use_ml and model_bundle:
        features = df[["rsi", "sma_fast", "sma_slow", "macd", "macd_signal", "macd_diff"]]
        df["signal"] = model_bundle["model"].predict(features)
    else:
        df["signal"] = df.apply(rule_based_signal, axis=1)

    return df
