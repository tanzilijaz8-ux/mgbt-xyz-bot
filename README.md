# MGBT XYZ — AI Signal Bot (Signals Only)

**Purpose:** Generate trading signals from market data using a hybrid approach:
- Rule-based technical strategy (SMA crossover, RSI, MACD)
- Optional ML classifier (Logistic Regression) trained on engineered features

**Safety & Compliance**
- This project **does not** place trades or connect to brokers.
- It **does not** automate Quotex or any other broker. If you trade, do so **manually**.
- For education only; no financial advice. Use at your own risk.

---

## Features
- Fetch OHLCV with `yfinance` (crypto via Yahoo tickers, equities/forex as available).
- Compute indicators with `ta`.
- Rule-based signals out-of-the-box.
- Optional ML training (`train.py`) -> saves `model.pkl`.
- Outputs to `signals.csv` and prints to console.
- Optional Telegram notifications (if you add credentials).

## Quick Start
```bash
# 1) Create a virtual env (recommended)
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Configure
cp .env.example .env   # set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID if you want alerts
# Or edit config.json for symbol/interval/period

# 4) Run rule-based signals now
python bot.py

# 5) (Optional) Train ML model first, then run bot with ML
python train.py
python bot.py --use-ml
```

## Config
Edit `config.json`:
```json
{
  "symbol": "BTC-USD",
  "period": "60d",
  "interval": "15m",
  "rsi_period": 14,
  "sma_fast": 10,
  "sma_slow": 30,
  "macd_fast": 12,
  "macd_slow": 26,
  "macd_signal": 9,
  "telegram_enabled": false
}
```

## Notes
- Yahoo Finance availability varies by instrument. Try symbols like `BTC-USD`, `ETH-USD`, `EURUSD=X`, `AAPL`.
- For ML, the model is a simple logistic regression baseline; extend as you like.
- This project intentionally avoids broker APIs and trade execution for safety.
