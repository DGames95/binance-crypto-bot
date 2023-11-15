from abc import ABC, abstractmethod
from enum import Enum

class TimeFrame(Enum):
    SECOND: int = 1
    MINUTE: int = 60
    HOUR: int = 3600
    DAY: int
    WEEK: int

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