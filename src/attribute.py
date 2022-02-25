from abc import ABC, abstractmethod
import tuple_obj

class Attribute(ABC):

    #returns true if this attribute is a quasi-identifier
    @abstractmethod
    def isQI():
        return False

    #return the value of this attribute in the given tuple
    @abstractmethod
    def getValue(tuple):
        return NotImplementedError

    #returns the generalized value of this attribute according to given range
    @abstractmethod
    def getGeneralization(range):
        return NotImplementedError

    

    
