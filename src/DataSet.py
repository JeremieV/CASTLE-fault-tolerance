
#public class
#contains information regarding the csv of a given file
from contextlib import nullcontext

#public class
#represents the data set contained in a CSV file
#iterate through this like:
# row = data.getNextTuple()
# while(row!=null):
#   #Do stuff
#   row = data.getNextTuple()
class DataSet:
    csvreader = None

    def __init__(self,fileName):
        pass

    #returns a tuple of attributes
    def getHeader(self):
        next(self.csvreader)
        pass

    def getNextRow(self):
        pass