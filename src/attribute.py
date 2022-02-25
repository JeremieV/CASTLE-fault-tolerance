from abc import ABC, abstractmethod
#I miss Java and c#

#public abstract class
class Attribute(ABC):
    QI = False
    index = -1
    name = ""

    #returns true if this attribute is a quasi-identifier
    def isQI(self):
        return self.QI

    #return the value of this attribute in the given tuple
    def getValue(self,tuple):
        if (self.index<0):
            return NotImplementedError
        else:
            return tuple[self.index]

    def getName(self):
        return self.name

    #returns the generalized value of this attribute according to given range
    @abstractmethod
    def getGeneralization(self,range):
        return NotImplementedError

#private class
#continous attributes
class _ContinousAttributes(Attribute):
    min
    max
    def __init__(self,name,index):
        self.name = name
        self.index = index



#public class responsible for creating the attribute objects
class AttributeFactory:

    #TO DO
    #Call this to create a tuple of attribute objects 
    #from the first row of file
    def createAttribute(name,index,QI,DHG=None):
        return None





    

    
