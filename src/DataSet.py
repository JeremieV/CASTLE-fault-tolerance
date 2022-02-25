from contextlib import nullcontext
import csv

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

    #returns a tuple of attributes
    def getHeader(self,row):
        #create the tuple of attributes
        return tuple()

    def getNextRow(self):
        return next(self.csvreader)