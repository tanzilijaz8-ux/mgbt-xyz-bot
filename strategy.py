import pandas as pd

def rule_based_signal(row: pd.Series) -> str:
    """
    Simple ensemble of signals:
    - SMA crossover: fast > slow -> buy; fast < slow -> sell
    - RSI < 30 -> buy bias; RSI > 70 -> sell bias
    - MACD hist > 0 -> buy bias; < 0 -> sell bias
    Final: majority vote among these hints.
    """
    votes = 0
    # SMA
    if row["sma_fast"] > row["sma_slow"]:
        votes += 1
    elif row["sma_fast"] < row["sma_slow"]:
        votes -= 1
    # RSI
    if row["rsi"] < 30:
        votes += 1
    elif row["rsi"] > 70:
        votes -= 1
    # MACD
    if row["macd_hist"] > 0:
        votes += 1
    elif row["macd_hist"] < 0:
        votes -= 1

    if votes > 0:
        return "BUY"
    elif votes < 0:
        return "SELL"
    else:
        return "HOLD"
