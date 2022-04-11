from binance.client import Client
from constants import API_KEY, API_SECRET
from action_functions import test_trade, execute_sell, execute_buy
from dataframe_functions import get_df
from model import predict, prep_data_model, train_model


# code outline:
# model inputs required to make decision: 13 prev hourly price + volume points, bitcoin price usdt,

# numpy is continously being a pain by storing numbers as strings or it's own datatype -
# if you see type error rerunning will usually fix, as will adding an explicit conversion to float or int


# initialise variables
test = True  # if True will perform trades in a csv only, no real trade orders placed
train = False  # if True, the model will train itself on the dataset first
ticker = 'ADA'
data_labels = ['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'quote asset volume',
                   'num trades', 'taker buy base asset volume', 'taker buy quote asset volume', 'ignore']

# initialise client and dataframes
print(f'initialising client...\ntrading {ticker}.')
if test:
    print('test mode enabled.\n')
client = Client(API_KEY, API_SECRET)
bitcoin_df, crypto_df = get_df(client, ticker, data_labels)

# get the data into correct format for model
X_scaled, Y = prep_data_model(crypto_df, bitcoin_df)

# if we set the train setting to true, will will train the model first
if train:
    train_model(ticker, X_scaled, Y)

# adjust data and make a prediction
prediction = predict(ticker, X_scaled)
print('predicted probabibilty of price increase = ' + str(round((prediction-0.5)*2, 2)) +
      '. (raw=' + str(round(prediction, 2)) + ')\n')

# now check the balance and compsition of the account
# NOTE: all trades are done in terms of USDT
current_crypto_price = float(client.get_avg_price(symbol='ADAUSDT').get('price'))

if not test:
    print('checking balances...')
    crypto_balance = float(client.get_asset_balance(asset=f'{ticker}').get('free'))
    usdt_balance = float(client.get_asset_balance(asset='USDT').get('free'))
else:
    # TODO: create a test wallet that records the worth
    crypto_balance = 500
    usdt_balance = 500

if (crypto_balance > 50/current_crypto_price) or (usdt_balance > 50):  # quick check if enough money
    print('USDT balance = ' + str(usdt_balance) + f', {ticker} balance = ' + str(crypto_balance) + '.\n')
else:
    print('WARNING: low funds.')
    print('USDT balance = ' + str(usdt_balance) + f', {ticker} balance = ' + str(crypto_balance) + '.\n')


# execute logic for buying, also checks whether we are just testing or if we actually want to connect to the account
if usdt_balance > 50 and prediction > 0.9:
    if test:
        test_trade('BUY', ticker, usdt_balance, current_crypto_price)
    else:
        execute_buy(ticker, usdt_balance, current_crypto_price)
elif crypto_balance > 50/current_crypto_price and prediction < 0.5:
    if test:
        test_trade('SELL', ticker, crypto_balance, current_crypto_price)
    else:
        execute_sell(ticker, crypto_balance, current_crypto_price)
else:
    print('no trade order created.')

# TODO: create a system to check no outstanding trade orders are left
# TODO: implement security measures to stop draining funds if left unnattended
# orders = client.get_open_orders(symbol='BNBBTC')

# TODO: create a way to run main every hour (probably on raspberry pi in future)


