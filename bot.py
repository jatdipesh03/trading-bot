import ccxt
import os
import time
import threading
from flask import Flask

app = Flask(__name__)

print("SERVER STARTED")

# Exchange connection
exchange = ccxt.delta({
    "apiKey": os.getenv("DELTA_API_KEY"),
    "secret": os.getenv("DELTA_API_SECRET"),
    "enableRateLimit": True
})

symbol = "BTC/USDT"

def trading_loop():
    print("TRADING LOOP STARTED")

    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            price = ticker["last"]

            print("BTC PRICE:", price)

        except Exception as e:
            print("BOT ERROR:", e)

        time.sleep(10)


def start_background_bot():
    bot_thread = threading.Thread(target=trading_loop)
    bot_thread.daemon = True
    bot_thread.start()


@app.route("/")
def home():
    return "Algo Bot Running"


if __name__ == "__main__":
    start_background_bot()
    app.run(host="0.0.0.0", port=10000)
