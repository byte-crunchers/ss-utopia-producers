import datetime
import json
import os
import shutil
import time

import numpy as np


class Stock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


stocks = (  # stock objects ready to be JSONized
    Stock(ticker="AMD", name="Advanced Micro Devices", price=110.25, marketCap=135030000, volume=60925000, PE=39.75,
          dividendYield=0, dividendRate=0, yearHigh=122.49, yearLow=72.50, open=111.19, high=111.21, low=109.03),
    Stock(ticker="INTC", name="Intel", price=54.21, marketCap=135030000, volume=60925000, PE=39.75, dividendYield=0,
          dividendRate=0, yearHigh=122.49, yearLow=72.50, open=111.19, high=111.21, low=109.03)
    # ["TSM", "Taiwan Semiconductor Manufacturing", 119.22],
    # ["MSFT", "Microsoft", 13.25],
    # ["VNM", "VanEck Vietnam ETF",19.75]
)


def clean():
    try:
        shutil.rmtree("stock_dump")  # rm -rf stock_dump
    except:
        print(
            "error deleating stock dump. Ignore if 'stock_dump/' didn't already exist")  # should be safe to ignore if dump didn't already exist

    os.mkdir("stock_dump")


def produce(numberOfFiles, delay):
    for i in range(1, numberOfFiles + 1):
        # print (i)
        for stock in stocks:
            path = "stock_dump/{ticker}{num:d}.json".format(ticker=stock.ticker, num=i)
            f = open(path, "w")  # opens i.json if exists, creates it if not
            change = np.random.normal(loc=1, scale=0.001)  # normal distribution with an SD of 1%
            stock.price *= change
            stock.marketCap *= change
            stock.timestamp = datetime.datetime.now().__str__()
            f.write(json.dumps(stock.__dict__,
                               indent=4))  # converts stock object to a dictionary, encodes it with JSON, and writes it to file
        time.sleep(delay)


if __name__ == "__main__":
    clean()
    produce(20, 0)
