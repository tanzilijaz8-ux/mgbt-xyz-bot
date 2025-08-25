import argparse, json, os
import pandas as pd
import joblib
from datetime import datetime

from data import fetch_ohlcv
from features import add_indicators
from strategy import rule_based_signal
from notifier import send_telegram

def generate_signals(df: pd.DataFrame, use_ml: bool, model_bundle: dict | None):
    signals = []
    for ts, row in df.iterrows():
        sig_rule = rule_based_signal(row)
        sig_ml = None
        final = sig_rule
        if use_ml and model_bundle:
            scaler = model_bundle["scaler"]
            clf = model_bundle["model"]
            feature_cols = model_bundle["features"]
            X = row[feature_cols].values.reshape(1, -1)
            Xs = scaler.transform(X)
            pred = int(clf.predict(Xs)[0])
            sig_ml = {1:"BUY", -1:"SELL", 0:"HOLD"}[pred]
            # Combine: if both agree -> use it; else HOLD to reduce churn
            final = sig_rule if sig_rule == sig_ml else "HOLD"

        signals.append({
            "timestamp": ts.isoformat(),
            "close": float(row["Close"]),
            "signal_rule": sig_rule,
            "signal_ml": sig_ml if use_ml else None,
            "final_signal": final
        })
    return pd.DataFrame(signals)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-ml", action="store_true", help="Use trained ML model.pkl if available")
    args = parser.parse_args()

    with open("config.json","r") as f:
        cfg = json.load(f)

    df = fetch_ohlcv(cfg["symbol"], cfg["period"], cfg["interval"])
    df = add_indicators(df, cfg["rsi_period"], cfg["sma_fast"], cfg["sma_slow"],
                        cfg["macd_fast"], cfg["macd_slow"], cfg["macd_signal"])

    model_bundle = None
    if args.use_ml and os.path.exists("model.pkl"):
        model_bundle = joblib.load("model.pkl")

    sigs = generate_signals(df, args.use_ml, model_bundle)

    out_path = "signals.csv"
    sigs.to_csv(out_path, index=False)
    print(f"Saved {out_path} with {len(sigs)} rows. Last 5 rows:")
    print(sigs.tail())

    # Send last signal to Telegram if enabled
    if cfg.get("telegram_enabled", False):
        last = sigs.iloc[-1]
        msg = f"[{cfg['symbol']}] {last['timestamp']} Close={last['close']:.4f} Signal={last['final_signal']}"
        ok = send_telegram(msg)
        print("Telegram sent:", ok)

if __name__ == "__main__":
    main()
