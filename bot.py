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

def trading_bot():

    print("BOT LOOP STARTED")

    while True:

        try:

            ticker = exchange.fetch_ticker(symbol)
            price = ticker["last"]

            print("BTC PRICE:", price)

        except Exception as e:

            print("ERROR:", e)

        time.sleep(10)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":

    thread = threading.Thread(target=trading_bot)
    thread.start()

    app.run(host="0.0.0.0", port=10000)
