# binance-crypto-bot

A bot that is able to keep an up to date database of prices and place trade orders based on advice from an LSTM neural net. 
Feel free to use parts of it to build models of your own, but don't use the bot as is, because it is a very basic model created for a learning experience and far from ideal. 

Bot gets the API keys from a file constants.py, for obvious reasons I do not include my own.

## TODO list:
1. validation
   
- validate model in more rigorously by determining precision, recall, f1 value
- test on definitely predictable data e.g. sin
