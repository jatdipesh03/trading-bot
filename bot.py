import requests
import time

balance = 10000
position = None
entry_price = 0

take_profit = 40
stop_loss = 20

prices = []

url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


def ema(data, period):
    k = 2 / (period + 1)
    ema_value = sum(data[:period]) / period

    for price in data[period:]:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value


while True:

    r = requests.get(url)
    data = r.json()

    print(data)

    if "price" not in data:
        time.sleep(5)
        continue

    price = float(data["price"])

    prices.append(price)

    if len(prices) > 50:
        prices.pop(0)

    if len(prices) > 21:

        ema9 = ema(prices[-9:], 9)
        ema21 = ema(prices[-21:], 21)

        print("Price:", price)
        print("EMA9:", ema9)
        print("EMA21:", ema21)

        if ema9 > ema21 and position is None:
            position = "BUY"
            entry_price = price
            print("BUY at", price)

        elif ema9 < ema21 and position == "BUY":
            profit = price - entry_price
            balance += profit
            position = None
            print("SELL at", price, "Profit:", profit)

    time.sleep(5)
