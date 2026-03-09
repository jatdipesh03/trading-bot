import requests
import time
import csv

balance = 10000
position = None
entry_price = 0

take_profit = 40
stop_loss = 20

prices = []

url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

def ema(data, period):
    k = 2 / (period + 1)
    ema_value = data[0]

    for price in data:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value


while True:

    r = requests.get(url)
    data = r.json()

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
            print("DEMO BUY at", price)

        if position == "BUY":

            profit = price - entry_price

            if profit >= take_profit:
                balance += profit
                print("TAKE PROFIT HIT")
                print("Profit:", profit)
                print("Balance:", balance)
                position = None

            elif profit <= -stop_loss:
                balance += profit
                print("STOP LOSS HIT")
                print("Loss:", profit)
                print("Balance:", balance)
                position = None

        print("----------------------")


    time.sleep(5)

