import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

prices = []

url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


def ema(data, period):
    k = 2 / (period + 1)
    ema_value = sum(data[:period]) / period

    for price in data[period:]:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value


def trading_bot():
    while True:
        try:
            r = requests.get(url)
            data = r.json()

            print("API Response:", data)

            price = float(data.get("price", 0))

            prices.append(price)

            if len(prices) > 50:
                prices.pop(0)

            if len(prices) > 21:
                ema9 = ema(prices[-9:], 9)
                ema21 = ema(prices[-21:], 21)

                print("Price:", price)
                print("EMA9:", ema9)
                print("EMA21:", ema21)

        except Exception as e:
            print("Error:", e)

        time.sleep(5)


@app.route("/")
def home():
    return "Trading Bot Running"


if __name__ == "__main__":
    threading.Thread(target=trading_bot).start()
    app.run(host="0.0.0.0", port=10000)
