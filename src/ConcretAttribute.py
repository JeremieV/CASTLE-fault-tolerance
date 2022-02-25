#This file contains concret implementations of the abstract Attribute object
#and shouldn't really be called outside of AttributeFactory

from Attribute import Attribute

#private class
#concret implementation of Attribute, represents continous attributes
class _ContinousAttributes(Attribute):

    def __init__(self,name,index):
        self.name = name
        self.index = index

       
    def createRange(self,values):
        min = min(values)
        max = max(values)
        result = (min,max)
        return result

    def expandRange(self,range,value):
        min = range[0]
        max = range[1]
        result = None
        if (value<min):
            result = (value,range[1])
        elif (value>max):
            result = (range[0],value)
        else:
            result = range
        return result