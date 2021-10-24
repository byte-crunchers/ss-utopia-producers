import datetime
import json
import os
import random
import time
import traceback

import boto3
import pandas as pd
from botocore.config import Config

access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

my_config = Config(
    region_name='us-east-1'
)


class Stock:
    def __init__(self, ticker, name, price, market_cap, volume, high, low, volatility, percent_change):
        self.percent_change = percent_change
        self.ticker = ticker
        self.name = name
        self.price = price
        self.market_cap = market_cap
        self.volume = volume
        self.high = high
        self.low = low
        self.timestamp = datetime.datetime.now()
        self.volatility = volatility

    def print_stock(self):
        print(self.ticker, self.name, self.price, self.market_cap, self.volume, self.high, self.low, self.volatility,
              self.percent_change, sep=" || ")


# Parse csv into Stocks using pandas
def get_initial_stock(file, num_of_stocks):
    init_stocks = []
    for _ in range(0, num_of_stocks):
        try:
            lp_list = pd.read_csv(file)
            pd_stock = lp_list.sample()
            pd.set_option('display.max_columns', None)
            volatility = round(random.uniform(0.02, 0.05), 2)
            initial_stock = Stock(pd_stock.iat[0, 0], pd_stock.iat[0, 1], float(pd_stock.iat[0, 2].strip("$")),
                                  pd_stock.iat[0, 5], pd_stock.iat[0, 8], float(pd_stock.iat[0, 2].strip("$")),
                                  float(pd_stock.iat[0, 2].strip("$")), volatility, None)
            init_stocks.append(initial_stock)
        except:
            traceback.print_exc()
    return init_stocks


# Update stock price based on volatile number algorithm and stream to kinesis
def update_stock(upd_stocks, interval_in_seconds):
    while True:
        for stock in upd_stocks:
            # stock.print_stock()
            print(str(stock.ticker) + " price: " + str(stock.price))
            rnd = round(random.uniform(0, 1), 2)
            change_percent = 2 * stock.volatility * rnd
            if change_percent > stock.volatility:
                change_percent -= (2 * stock.volatility)
            change_amount = stock.price * change_percent
            if stock.price + change_amount < 0:
                continue  # If the next step would result in a negative price, redo change calculation
            new_price = stock.price + change_amount
            if new_price > stock.high:
                stock.high = round(new_price, 2)
            if new_price < stock.low:
                stock.low = round(new_price, 2)
            stock.price = round(new_price, 4)
            stock.percent_change = round(change_percent, 4)
            # Send stock data to Kinesis stream
            try:
                kin = boto3.client('kinesis', config=my_config, aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_key)
                print(json.dumps(stock.__dict__, default=str))
                stock.type = 'stock'  # for the consumer to know what type of message it is
                kin.put_record(StreamName='byte-henry', Data=json.dumps(stock.__dict__, default=str),
                               PartitionKey='trans key')
            except:
                traceback.print_exc()
        time.sleep(2)


if __name__ == '__main__':
    stocks = get_initial_stock("nasdaq_tickers.csv", 1)
    update_stock(stocks, 2)
