import random
import time
import traceback

import pandas as pd


class Stock:
    def __init__(self, ticker, name, price, market_cap, volume, high, low):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.market_cap = market_cap
        self.volume = volume
        self.high = high
        self.low = low

    def print_stock(self):
        print(self.ticker, self.name, self.price, self.market_cap, self.volume, self.high, self.low, sep=" || ")


# Parse csv into Stocks using pandas
def get_initial_stock(file, num_of_stocks):
    init_stocks = []
    for _ in range(0, num_of_stocks):
        try:
            lp_list = pd.read_csv(file)
            pd_stock = lp_list.sample()
            pd.set_option('display.max_columns', None)
            intial_stock = Stock(pd_stock.iat[0, 0], pd_stock.iat[0, 1], float(pd_stock.iat[0, 2].strip("$")),
                                 pd_stock.iat[0, 5], pd_stock.iat[0, 8], float(pd_stock.iat[0, 2].strip("$")),
                                 float(pd_stock.iat[0, 2].strip("$")))
            init_stocks.append(intial_stock)
        except:
            traceback.print_exc()
    return init_stocks


# Update stock price based on volatile number algorithm
def update_stock(upd_stocks, interval_in_seconds):
    while True:
        for stock in upd_stocks:
            stock.print_stock()

            volatility = round(random.uniform(0.02, 0.08), 2)
            rnd = round(random.uniform(0, 1), 2)
            change_percent = 2 * volatility * rnd
            if change_percent > volatility:
                change_percent -= (2 * volatility)
            change_amount = stock.price * change_percent
            new_price = stock.price + change_amount

            if new_price > stock.high:
                stock.high = round(new_price, 2)
            if new_price < stock.low:
                stock.low = round(new_price, 2)
            stock.price = round(new_price, 2)
            time.sleep(2)


if __name__ == '__main__':
    stocks = get_initial_stock("nasdaq_tickers.csv", 1)
    update_stock(stocks, 2)
