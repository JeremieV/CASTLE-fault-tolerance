from ast import Import
from contextlib import nullcontext
import csv
from attribute import Attribute,AttributeFactory

#public class
#represents the data set contained in a CSV file
#iterate through this like:
# row = data.getNextTuple()
# while(row!=null):
#   #Do stuff
#   row = data.getNextTuple()
class DataSet:
    csvreader = None
    myHeader = None

    def __init__(self,file):
        csv_reader = csv.reader(file)
        row = next(csv_reader)
        self.myHeader = self.getHeader(row)

    #public method
    #returns a tuple of attributes
    def getHeader(self,row):
        resultList = []
        i = 0
        for column in row:
            name = column
            index = i
            i += 1
            QI = self._isQI(column)
            resultList.append(AttributeFactory.createAttribute(name,index,QI))
        return tuple(resultList)

    #private method
    #returns true if the column is a quasi-identifier
    def _isQI(self,columnName):
        return True

    #public method
    #returns the next tuple
    def getNextRow(self):
        return next(self.csvreader)