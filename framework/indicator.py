from abc import ABC, abstractmethod
from enum import Enum

from data_tools import Prediction, PriceSeries


class Indicator(ABC):
    """
    An indicator takes a series of data and returns a prediction
    """
    
    @abstractmethod
    def evaluate(self, PriceSeries) -> Prediction:
        pass
    
    

    