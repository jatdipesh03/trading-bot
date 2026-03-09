import ccxt
import os
import time
import threading
from flask import Flask

app = Flask(__name__)

print("SERVER STARTED")

exchange = ccxt.delta()

symbol = "BTC/USDT"

def bot_loop():
    print("BOT LOOP STARTED")
    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            print("BTC PRICE:", ticker["last"])
        except Exception as e:
            print("ERROR:", e)

        time.sleep(10)

@app.route("/")
def home():
    return "Bot Running"

if __name__ == "__main__":
    t = threading.Thread(target=bot_loop)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=10000)
