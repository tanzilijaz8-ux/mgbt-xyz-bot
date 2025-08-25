import yfinance as yf
import pandas as pd

def fetch_ohlcv(symbol: str, period: str = "60d", interval: str = "15m") -> pd.DataFrame:
    df = yf.download(tickers=symbol, period=period, interval=interval, auto_adjust=True, progress=False)
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise RuntimeError(f"No data returned for {symbol} {period=} {interval=}")
    df = df.rename(columns=str.title)  # Open, High, Low, Close, Volume
    df = df.dropna()
    return df
