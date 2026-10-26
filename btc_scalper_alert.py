import os
import requests
import pandas as pd

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API = "https://api.binance.com/api/v3/klines"

def send_message(message):
    if not TOKEN or not CHAT_ID:
        raise ValueError("Les secrets Telegram ne sont pas configurés.")
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message},
        timeout=15
    )
    response.raise_for_status()

def check_market():
    response = requests.get(
        API,
        params={"symbol": "BTCUSDT", "interval": "5m", "limit": 100},
        timeout=15
    )
    response.raise_for_status()
    candles = response.json()

    df = pd.DataFrame(candles, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades",
        "taker_base", "taker_quote", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    df = df.iloc[:-1].copy()

    df["ema9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema21"] = df["close"].ewm(span=21, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()

    previous, current = df.iloc[-2], df.iloc[-1]
    signal = None

    if previous.ema9 <= previous.ema21 and current.ema9 > current.ema21 and current.close > current.ema50:
        signal = "ACHAT"
    elif previous.ema9 >= previous.ema21 and current.ema9 < current.ema21 and current.close < current.ema50:
        signal = "VENTE"

    if signal:
        send_message(
            f"🔔 Signal BTC/USDT : {signal}\n"
            f"Prix indicatif Binance : {current.close:.2f} USDT\n"
            "⚠️ Signal expérimental, à vérifier avant toute décision."
        )
        print(f"Signal envoyé : {signal}")
    else:
        print("Aucun nouveau signal.")

if __name__ == "__main__":
    check_market()
