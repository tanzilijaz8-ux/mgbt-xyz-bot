import pandas as pd
import ta

def add_indicators(df, rsi_period, sma_fast, sma_slow, macd_fast, macd_slow, macd_signal):
    out = df.copy()

    # Ensure "Close" is a clean 1D float Series
    close = pd.to_numeric(out["Close"].squeeze(), errors="coerce")

    # RSI
    out["rsi"] = ta.momentum.RSIIndicator(close=close, window=rsi_period).rsi()

    # SMA
    out["sma_fast"] = ta.trend.SMAIndicator(close=close, window=sma_fast).sma_indicator()
    out["sma_slow"] = ta.trend.SMAIndicator(close=close, window=sma_slow).sma_indicator()

    # MACD
    macd = ta.trend.MACD(
        close=close,
        window_slow=macd_slow,
        window_fast=macd_fast,
        window_sign=macd_signal
    )
    out["macd"] = macd.macd()
    out["macd_signal"] = macd.macd_signal()
    out["macd_diff"] = macd.macd_diff()

    return out

