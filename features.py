import pandas as pd
import numpy as np
import ta

def add_indicators(df: pd.DataFrame,
                   rsi_period: int = 14,
                   sma_fast: int = 10,
                   sma_slow: int = 30,
                   macd_fast: int = 12,
                   macd_slow: int = 26,
                   macd_signal: int = 9) -> pd.DataFrame:
  out = df.copy()
# RSI
out["rsi"] = ta.momentum.RSIIndicator(
    close=out["Close"].astype(float).squeeze(),
    window=rsi_period).rsi()
    # SMAs
    out["sma_fast"] = out["Close"].rolling(sma_fast).mean()
    out["sma_slow"] = out["Close"].rolling(sma_slow).mean()
    # MACD
    macd = ta.trend.MACD(close=out["Close"], window_fast=macd_fast, window_slow=macd_slow, window_sign=macd_signal)
    out["macd"] = macd.macd()
    out["macd_signal"] = macd.macd_signal()
    out["macd_hist"] = macd.macd_diff()

    # Volatility / returns
    out["ret_1"] = out["Close"].pct_change()
    out["ret_5"] = out["Close"].pct_change(5)
    out["ret_10"] = out["Close"].pct_change(10)
    out["volatility_10"] = out["ret_1"].rolling(10).std()

    out = out.dropna()
    return out

def make_ml_dataset(df: pd.DataFrame, horizon: int = 3, threshold: float = 0.002):
    """
    Create labels: 1 if future return over horizon > threshold, -1 if < -threshold, else 0.
    """
    out = df.copy()
    future = out["Close"].shift(-horizon)
    future_ret = (future - out["Close"]) / out["Close"]
    y = future_ret.apply(lambda r: 1 if r > threshold else (-1 if r < -threshold else 0))
    feature_cols = ["rsi","sma_fast","sma_slow","macd","macd_signal","macd_hist","ret_1","ret_5","ret_10","volatility_10"]
    X = out[feature_cols].values
    mask = ~pd.isna(y)
    return X[mask], y[mask].values, feature_cols
