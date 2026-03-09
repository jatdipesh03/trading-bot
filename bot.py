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
    "enableRateLimit": True,
})

symbol = "BTC/USDT:USDT"


def trading_loop():

    print("TRADING LOOP STARTED")

    while True:

        try:

            print("FETCHING PRICE...")

            ticker = exchange.fetch_ticker(symbol)

            print("PRICE RECEIVED")

            price = ticker["last"]

            print("BTC PRICE:", price)

        except Exception as e:

            print("BOT ERROR:", str(e))

        time.sleep(10)


@app.route("/")
def home():
    return "Algo Bot Running"


if __name__ == "__main__":

    thread = threading.Thread(target=trading_loop)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=10000)
