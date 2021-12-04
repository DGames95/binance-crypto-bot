# action_functions contains all actions that can be taken based on the model predictions
from os.path import exists
from main import client
from binance.enums import *
import pandas as pd
import numpy as np
import time


# for the logs of trade orders placed
columns = ['time', 'ticker', 'action', 'amount usdt', 'amount crypto', 'price per item']


# NOTE: the price is always the crypto price in usd
# NOTE: amount refers to the amount of usdt to buy with in a buy scenario, and amount of crypto to sell in sell scenario
def execute_buy(ticker, amount, price):
    client.create_order(
        symbol=f'{ticker}USDT',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=amount,
        price=price)


def execute_sell(ticker, amount, price):
    client.create_order(
        symbol=f'{ticker}USDT',
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=amount,
        price=price)


def test_trade(action, ticker, amount, price):
    buy_string = 'placing test buy order of ' + str(round(amount/price, 2)) + f' {ticker} for $' + str(amount) + '.'
    sell_string = 'placing test sell order of ' + str(amount) + f' {ticker} for $' + str(round(amount * price, 2)) + '.'
    if action == 'BUY':
        print(buy_string)
        entry = np.array([[time.time(), ticker, action, amount, amount / price, price]])
    else:
        entry = np.array([[time.time(), ticker, action, amount*price, amount, price]])
        print(sell_string)

    if exists(f'data/test-trades-{ticker}.csv'):
        print('test trade data found, appending current trade...')
        with open(f'data/test-trades-{ticker}.csv') as f:
            test_trade_df = pd.read_csv(f)
        test_trade_df = test_trade_df.append(pd.DataFrame(entry, columns=columns))
    else:
        print('no test data found, creating new...')
        test_trade_df = pd.DataFrame(entry, columns=columns)

    test_trade_df.to_csv(f'data/test-trades-{ticker}.csv', index=False)


def log_action(action):
    columns = ['time']
    entry = [[time.time()]]  # TODO: create a log of all predictions and actions, including non-action.
