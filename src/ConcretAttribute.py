#This file contains concret implementations of the abstract Attribute object
#and shouldn't really be called outside of AttributeFactory

import sys
from typing import Tuple
from Attribute import Attribute
from DHG import DHG

#private class
#concret implementation of Attribute, represents continous attributes
class _ContinousAttributes(Attribute):

    #defines the domain of this attribute
    #all values of the attribute must fall within the domain
    domain = [0,sys.maxint]

    def __init__(self,name,index):
        self.name = name
        self.index = index
       
    def createRange(self,values)->Tuple:
        min = min(values)
        max = max(values)
        result = (min,max)
        return result

    def expandRange(self,range,value:Tuple)->Tuple:
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

    def calculateInfoLoss(self,range)->float:
        min = range[0]
        max = range[1]
        return (max-min)/(self.domain[1]-self.domain[0])

    def getDomain(self):
        return self.domain


    def getGeneralization(self, range=None):
        if (range is None):
            return str(self.getDomain()[0])+"<=x<="+str(self.getDomain()[1])
        min = range[0]
        max = range[1]
        result = str(min)+"<=x<="+str(max)

#private class
#concret implementation of Attribute, represents catagorical attributes
class _CategoricalAttributes(Attribute):
    DHG:DHG = None
    LeftTraversal = None

    def __init__(self,name:str,index:int,DHG:DHG):
        self.name = name
        self.index = index
        self.DHG = DHG
        self.LeftTraversal = self.DHG.getLeftTraversal()


    def calculateInfoLoss(self,range)->float:
        min = range[0]
        max = range[1]

        total = self.DHG.countLeaves()
        return (max-min)/(total-1)

    def createRange(self,values:List[Tuple])->Tuple:
        min = None
        max = None
        minRank = self.LeftTraversal.len() 
        maxRank = -1
        for element in values:
            rank = self.LeftTraversal.index(element)
            if (rank<minRank):
                min = rank
            elif(rank>maxRank):
                max = rank

        result = (min,max)
        return result

    def expandRange(self,range,value:Tuple)->Tuple:
        min = range[0]
        max = range[1]
        
        minRank = self.LeftTraversal.index(min)
        maxRank = self.LeftTraversal.index(max)
        valueRank = self.LeftTraversal.index(value)

        result = None
        if (valueRank<minRank):
            result = (value,max)
        elif (valueRank>maxRank):
            result = (min,value)
        else:
            result = range
        return result

    

    def getGeneralization(self, range=None):
        if (range is not None):
            return self.getDHG().getLCA(range[0],range[1])
        else:
            return self.getDHG().getRoot()
