from abc import ABC, abstractmethod
from enum import Enum



class Prediction(Enum):
    DIRECTION: float
    PRICE: float
    SERIES: list[float]
    

class PriceSeries(ABC):
    @abstractmethod
    def day(self) -> list | None:
        pass
    
    @abstractmethod
    def week(self) -> list | None:
        pass