from abc import ABC, abstractmethod
from dataclasses import dataclass


class DataStream():
    pass

class PriceStream(DataStream):
    pass

class ModelTest():
    pass

@dataclass
class ValidationScore():
    precision: float
    recall: float
    f1: float
    

class Model(ABC):
    # where does it train? (maybe we can send it off to separate cloud service)
    aggression: float
    
    # once trained we need to save it, and we need to load the model when we want to use it
    
    @abstractmethod
    def validate(self) -> ValidationScore:
        pass
    
    @abstractmethod
    def train(data) -> None:
        pass
    
    @abstractmethod
    def predict() -> bool:
        pass
    
            

class Strategy():
    # a model is used to implement a strategy
    
    model: Model | None
    
    @abstractmethod
    def react(event):
        pass
    



@dataclass
class Asset():
    # required attributes
    name: str
    token: str  # what if token is different per exchange?
    
    @abstractmethod
    def convert():
        pass   
    
    
class AccountManager(ABC):
    exchange: str  # link to the of Exchange
    asset: Asset
    
    
    @property
    def balance(self):
        # return exchange.balancefunction
        pass
    
    
    # Remember you can in theory only place orders, the market may not fulfill request
    # take some time to understand how it works
    @abstractmethod
    def place_buy(self, amount) -> None:
        pass
    
    @abstractmethod
    def place_sell(self, amount) -> None:
        pass
    
    @abstractmethod
    def get_balance(self) -> float | str:
        pass
    
    @abstractmethod
    def add_percentage(self, item, percentage: int) -> None:
        # add percent of current cash to the item
        pass
    
    @abstractmethod
    def all_out(self, item, percentage: int) -> None:
        # take out percentage of value of asset
        pass
        
class Exchange(ABC):
    account_manager: AccountManager

    # store key information and interface for database
    
    pass
 


    
    
class TestTrades(AccountManager):
    pass

class BasicTrend(Strategy):
    def predict():
        # if price[prev] < price[current] return True else False
        pass

