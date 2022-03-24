#This file contains concret implementations of the abstract Attribute object
#and shouldn't really be called outside of AttributeFactory

import sys
from typing import Tuple,List
from Attribute import Attribute
from DHG import DHG
from DHGTreeNode import DHGTreeNode
from tupleWrapper import TupleWrapper


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

#private class
#concret implementation of Attribute, represents continous attributes
class _ContinousAttributes(Attribute):

    #defines the domain of this attribute
    #all values of the attribute must fall within the domain
    domain = [0,69696969]

    def __init__(self,name,index):
        self.name = name
        self.index = index
       
    def createRange(self,values)->Tuple:
        min = min(values)
        max = max(values)
        result = (min,max)
        return result

    def expandRange(self,range,value:Tuple)->Tuple:
        result = None
        if len(range) > 0:
            min = range[0]
            max = range[1]
            if (value<min):
                result = (value,range[1])
            elif (value>max):
                result = (range[0],value)
            else:
                result = range
        else:
            result = (value, value)
        return result

    def calculateInfoLoss(self,range)->float:
        if len(range) > 0:
            min = float(range[0])
            max = float(range[1])
            return (max-min)/(self.domain[1]-self.domain[0])
        return 0

    def getDomain(self):
        return self.domain


    def getGeneralization(self, range=None):
        if (range is None):
            return str(self.domain[0])+"<=x<="+str(self.domain[1])
        min = range[0]
        max = range[1]
        result = str(min)+"<=x<="+str(max)
        return result
    
    def calc_distance(self, tbar: TupleWrapper, t: TupleWrapper) -> float:
        v1:float = float(self.getValue(tbar))
        v2:float = float(self.getValue(t))
        pow(v1-v2, 2)

#private class
#concret implementation of Attribute, represents catagorical attributes
class _CategoricalAttributes(Attribute):
    LeftTraversal = None

    def __init__(self,name:str,index:int,dhg:DHG):
        self.name = name
        self.index = index
        self.myDHG = dhg
        self.LeftTraversal = self.myDHG.getLeftTraversal()


    def calculateInfoLoss(self,range)->float:
        if len(range) > 0:
            min = float(range[0])
            max = float(range[1])

            total = self.myDHG.countLeaves()
            if total == 1:
                return 0
            return (max-min)/(total-1)
        return 0

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
        result = None
        if len(range) > 0:
            min = range[0]
            max = range[1]
            
            minRank = self.LeftTraversal.index(min)
            maxRank = self.LeftTraversal.index(max)
            valueRank = self.LeftTraversal.index(value)

            if (valueRank<minRank):
                result = (value,max)
            elif (valueRank>maxRank):
                result = (min,value)
            else:
                result = range
        else:
            result = (value, value)
        return result

    

    def getGeneralization(self, range=None):
        if (range is not None):
            return self.getDHG().getLCA(range[0],range[1])
        else:
            return self.getDHG().getRoot()
    
    def calc_distance(self, tbar: TupleWrapper, t: TupleWrapper) -> float:
        val_1 = 0
        val_2 = 0
        for tree_node in self.LeftTraversal:
            if tree_node.value == self.getValue(tbar):
                val_1 = tree_node.index
                break

            elif tree_node.value == self.getValue(t):
                val_2 = tree_node.index
                break
        return pow(val_1-val_2, 2)
