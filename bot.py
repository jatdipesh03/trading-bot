import ccxt
import os
import time
import threading
from flask import Flask

app = Flask(__name__)

print("SERVER STARTED")

api_key = os.getenv("DELTA_API_KEY")
api_secret = os.getenv("DELTA_API_SECRET")

exchange = ccxt.delta({
    "apiKey": api_key,
    "secret": api_secret,
    "enableRateLimit": True
})

symbol = "BTC/USDT"

prices = []

def ema(data, period):
    k = 2 / (period + 1)
    ema_value = sum(data[:period]) / period

    for price in data[period:]:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value


def trading_bot():

    print("=== TRADING BOT STARTED ===")

    while True:
        try:

            ticker = exchange.fetch_ticker(symbol)
            price = ticker["last"]

            print("CURRENT PRICE:", price)

            prices.append(price)

            if len(prices) > 50:
                prices.pop(0)

            if len(prices) > 21:

                ema9 = ema(prices[-9:], 9)
                ema21 = ema(prices[-21:], 21)

                print("EMA9:", ema9)
                print("EMA21:", ema21)

                if ema9 > ema21:
                    print("BUY SIGNAL")

                if ema9 < ema21:
                    print("SELL SIGNAL")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(10)


@app.route("/")
def home():
    return "Algo Trading Bot Running"


if __name__ == "__main__":

    bot_thread = threading.Thread(target=trading_bot)
    bot_thread.daemon = True
    bot_thread.start()

    app.run(host="0.0.0.0", port=10000)
