#This file contains concret implementations of the abstract Attribute object
#and shouldn't really be called outside of AttributeFactory

from attribute import Attribute

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

    def getGeneralization(self, range):
        min = range[0]
        max = range[1]
        result = str(min)+"<=x<="+str(max)

#private class
#concret implementation of Attribute, represents catagorical attributes
class _CategoricalAttributes(Attribute):
    #TODO
    DHG = None
    LeftTraversal = None

    def __init__(self,name,index,DHG):
        self.name = name
        self.index = index
        self.DHG = DHG
        self.LeftTraversal = self.DHG.getLeftTraversal() #TODO


       
    def createRange(self,values):
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

    def expandRange(self,range,value):
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

    def getGeneralization(self, range):
        return self.DHG.getLowestCommonAncestor(range) #TODO