import numpy as np

def rule_based_signal(row):
    """
    Generate a simple trading signal based on SMA crossovers and RSI.
    Returns:
        1 = Buy
       -1 = Sell
        0 = Hold
    """

    # Ensure values are floats (not pandas Series)
    sma_fast = float(row["sma_fast"])
    sma_slow = float(row["sma_slow"])
    rsi = float(row["rsi"])
    macd = float(row["macd"])
    macd_signal = float(row["macd_signal"])

    # Example rules:
    if sma_fast > sma_slow and rsi < 70 and macd > macd_signal:
        return 1   # Buy signal
    elif sma_fast < sma_slow and rsi > 30 and macd < macd_signal:
        return -1  # Sell signal
    else:
        return 0   # Hold


def generate_signals(df, use_ml=False, model_bundle=None):
    """
    Generate trading signals for the entire DataFrame.
    If use_ml=True, it uses ML model predictions instead of rule-based signals.
    """
    if use_ml and model_bundle:
        # ML-based prediction
        features = df[["rsi", "sma_fast", "sma_slow", "macd", "macd_signal", "macd_diff"]]
        df["signal"] = model_bundle["model"].predict(features)
    else:
        # Rule-based strategy
        df["signal"] = df.apply(rule_based_signal, axis=1)

    return df
