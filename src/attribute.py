from abc import ABC, abstractmethod
import tuple_obj

class Attribute(ABC):

    @abstractmethod
    def isQI():
        return False

    @abstractmethod
    def getValue(tuple_obj):
        return NotImplementedError

    @abstractmethod
    def getGeneralization(range):
        return NotImplementedError

    

    
