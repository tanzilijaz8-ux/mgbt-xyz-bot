import json, os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

from data import fetch_ohlcv
from features import add_indicators, make_ml_dataset

def main():
    with open("config.json","r") as f:
        cfg = json.load(f)

    df = fetch_ohlcv(cfg["symbol"], cfg["period"], cfg["interval"])
    df = add_indicators(df, cfg["rsi_period"], cfg["sma_fast"], cfg["sma_slow"],
                        cfg["macd_fast"], cfg["macd_slow"], cfg["macd_signal"])
    X, y, feature_cols = make_ml_dataset(df, horizon=3, threshold=0.002)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    clf = LogisticRegression(max_iter=200, multi_class="ovr")
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.25, random_state=42, stratify=y)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump({"model": clf, "scaler": scaler, "features": feature_cols}, "model.pkl")
    print("Saved model.pkl")

if __name__ == "__main__":
    main()
