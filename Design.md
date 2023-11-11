### 11 Nov 2023

components

Trading Side
- storage of secrets for exchanges, provide utility for encryption before entering into db
- exchange class for stateless exchange info and methods
- account manager: interface with the exchange and store states of orders etc.
- provide either exchange centered or asset centered trading
- live and backtesting must be facilitated

each exchange has an account manager has a certain amount of money, assets they trade, compare multiple models. manager might have different security clearance? to prevent accidentally large purchases if the manager gets an unexpected result from the model?

overall accounts class that keeps track of all managers and total funds and balances

so, managers are stateful, and accounts class is stateful, all other trading classes are just used as functional classes

Data Side
- collect a database of price info that can be used for training
- real time updating of the database
- recognize data gaps and pull them automatically
- simulate data
- cleanly combine asset centered and exchange centered data

Model Side
- model can be split into deployment, development and tuning
- deployment and tuning must integrate in a CI fashion, running validation tests on each change
- development must facilitate proper validation techniques to qunatify performance

Deployment Side
- packaging
- cloud-ready
- optimization
- security - only decrypt keys on use, provide use of TPM for encryption


Nice To Haves
- combining multiple models for different situations, e.g. arbitrage and main trading model, short and long term strategy
- bullish/bearish meter that tones up or down aggressiveness in all models

