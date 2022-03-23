from abc import ABC, abstractmethod
from xmlrpc.client import boolean
from ConcretAttribute import _CategoricalAttributes,_ContinousAttributes
from __future__ import annotations
from tupleWrapper import TupleWrapper
from typing import Tuple,List,Dict
from DHG import DHG

#public abstract class
#Represents a column in the DataSet
#can perform certain calculations
#for example, calculating the range of a list of values
class Attribute(ABC):
    QI = False
    index = -1
    name = ""
    PID = False

    #returns true if this attribute is a quasi-identifier
    def isQI(self) -> bool:
        return self.QI

    #return the value of this attribute in the given tuple
    def getValue(self,tuple:TupleWrapper) ->str:
        if (self.index<0):
            return NotImplementedError
        else:
            return tuple[self.index]

    #returns the name of the column, used for printing
    def getName(self) -> str:
        return self.name

    
    def isPID(self)-> bool:
        return self.PID

    def getDHG(self) -> DHG:
        return self.DHG

    #returns the generalized value  (as a string)
    #of this attribute according to the given range
    #
    #This was meant to be used when outputting
    @abstractmethod
    def getGeneralization(self,range=None) ->str:
        return NotImplementedError

    
    #given a list of values,
    #return a tuple representing the range
    @abstractmethod
    def createRange(self,values:List)->Tuple:
        return NotImplementedError

    @abstractmethod
    #given the range as a tuple
    #return the information loss of a given generalization
    #
    #Note. the infoloss of a tuple is the average of the infoLoss of all its generalization
    def calculateInfoLoss(self,range) -> float:
        return NotImplementedError

    #given the current range (as a tuple of length 2) and new value
    #return the expanded range (as a tuple of length 2)
    @abstractmethod
    def expandRange(self,range,value:Tuple)->Tuple:
        return NotImplementedError



#public class responsible for instantiating the attribute objects
class AttributeFactory:

    #Call this to create a tuple of attribute objects 
    #from the first row of file
    #if a DHG is given, then we know this is a categorical attribute
    def createAttribute(name,index,QI,PID,DHG=None):
        result = None
        if (DHG==None):
            result = _ContinousAttributes(name,index)
        else:
            result = _CategoricalAttributes(name,index,DHG)
        result.PID=PID
        result.QI = QI
        return result





    

    
