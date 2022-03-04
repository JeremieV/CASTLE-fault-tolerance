from ast import Import
from contextlib import nullcontext
import csv
from Attribute import Attribute,AttributeFactory

#public class
#represents the data set contained in a CSV file
#describes the data stream
#iterate through this like:
# row = data.getNextTuple()
# while(row!=null):
#   #Do stuff
#   row = data.getNextTuple()
class DataSet:
    csvreader = None
    Headers = None
    definition = None

    def __init__(self,file,definition):
        self.csv_reader = csv.reader(file)
        row = next(self.csv_reader)
        self.definition=definition
        self.Headers = self.__createHeaders(row)

    #Returns the list of attributes which are quasi-identifiers
    def getQuasiIdentifiers(self):
        result = []
        for attri in self.Headers:
            if (attri.isQI()==True):
                result.append(attri)
        return result

    #Returns all attributes in this dataset
    def getAttributes(self):
        return self.Headers


    #public method
    #returns the next tuple
    def getNextRow(self):
        return next(self.csvreader)

    #private method
    #returns a tuple of attributes
    def _createHeaders(self,row):
        resultList = []
        i = 0
        for column in row:
            name = column
            index = i
            i += 1
            QI = self._isQI(column)
            DGH = self._getDGH(column)
            resultList.append(AttributeFactory.createAttribute(name,index,QI,DGH))
        return tuple(resultList)

    #private method
    #returns true if the column is a quasi-identifier
    def _isQI(self,columnName):
        return self.definition.isQI(columnName)

    #private method
    #returns the DGH of a column if it exists
    #otherwise, return None
    def _getDGH(self,columnName):
        return self.definition.getDGH(columnName)