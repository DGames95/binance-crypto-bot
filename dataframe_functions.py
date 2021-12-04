# contains the code for keeping the csv of price data upto date, and returning dataframes to be used
from os.path import exists
from datetime import datetime
import time
import pandas as pd
from binance.client import Client


def create_csv(client, ticker, data_labels):
    inputs = client.get_historical_klines(symbol=f"{ticker}USDT", start_str="5 days ago UTC",
                                          interval=Client.KLINE_INTERVAL_1HOUR)
    df = pd.DataFrame(inputs, columns=data_labels)
    # add another column with datetime date, for understanding and debugging purposes
    df['close datetime'] = [datetime.fromtimestamp(x / 1000) for x in df['close time'].to_list()]
    df.to_csv(f'data/{ticker}USDT-KLINES.csv', index=False)
    return df


def get_df(client, ticker, data_labels):
    # open csv file if it exists, then if the last time was 1 hour ago, then use this csv file as the dataframe and append current kline
    # this guarantees the data is up to date
    # NOTE: df refers to crypto_df, bitcoin_df to itself
    # NOTE: latest time always bottom(last) entry
    # NOTE: time from binance is in unix MILLISECONDS

    # for bitcoin, because it leads the market
    if exists(f'data/BTCUSDT-KLINES.csv'):
        print('btc csv exists.')
        with open(f'data/BTCUSDT-KLINES.csv') as f:
            bitcoin_df = pd.read_csv(f)

        if bitcoin_df['close time'].to_list()[-1] > int(time.time()*1000):
            bitcoin_df.to_csv(f'data/BTCUSDT-KLINES.csv', index=False)
            print('btc csv up to date.\n')
        else:
            print('btc csv out of date, creating new...\n')
            bitcoin_df = create_csv(client, 'BTC', data_labels)

    else:
        print('no btc csv available, creating...\n')
        bitcoin_df = create_csv(client, 'BTC', data_labels)

    # for the crypto in question
    if exists(f'data/{ticker}USDT-KLINES.csv'):
        print('crypto csv exists.')
        with open(f'data/{ticker}USDT-KLINES.csv') as f:
            df = pd.read_csv(f)

        if df['close time'].to_list()[-1] > int(time.time()*1000):
            df.to_csv(f'data/{ticker}USDT-KLINES.csv', index=False)
            print('crypto csv up to date.\n')
        else:
            print('crypto csv out of date, creating new...\n')
            df = create_csv(client, ticker, data_labels)

    else:
        print('no crypto csv available, creating new...\n')
        df = create_csv(client, ticker, data_labels)

    return bitcoin_df, df
