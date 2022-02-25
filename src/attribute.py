from abc import ABC, abstractmethod
import tuple_obj
#I miss Java and c#

#public abstract class
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

#public class responsible for creating the attribute objects
class AttributeFactory:

    #TO DO
    #Call this to create a tuple of attribute objects 
    #from the first row of file
    def createAttributes(row):
        return tuple()



    

    
