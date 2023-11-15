from framework import Bot
from framework.data_tools import Prediction, TimeFrame
from current_project.trading import Exchange1, Exchange2
# each exchange inherits from the exchange abc




bot = Bot

exchange1 = bot.init_exchange(Exchange1)

manager1 = bot.init_manager(exchange1)
manager1.load_capital(10000)

@manager1.indicator("lstm1")
def predict_item():
    # call you model from here
    return Prediction

@manager1.indicator("SMA1")
def predict_item():
    # call you model from here
    return Prediction


if __name__=="__main__":
    keys_db_pw = input("enter keys password")
    bot.run(keys_db_pw, train_interval=TimeFrame.DAY)

