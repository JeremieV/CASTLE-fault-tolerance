from DGHFactory import DGHFactory
from DataSet import DataSet

#describes information about a column 
#used in DataSet initialization
class ColumnDefinition:
    #dictionary to store if a column is a QI
    QIMap = {}
    #dictionary to store the DHG of a column
    DGHMap = {}

    def addDef(self,columnName,QI,DGH=None):
        self.QIMap[columnName] = QI
        if (DGH!=None):
            self.DGHMap[columnName] = DGH

    def isQI(self,columnName):
        return self.QIMap[columnName]

    def getDGH(self,columnName):
        if (columnName in self.DGHMap):
            return self.DGHMap[columnName]
        return None


#creates specific datasets
#this is Hardcoded
#
#creates the relavant column definition
#returns dataset obeject
class DataSetFactory:

    #data set for credit_data.csv
    def createCreditData(file):

        #clientid,income,age,loan,default
        definition = ColumnDefinition()
        definition.addDef("clientid",False)
        definition.addDef("age",True)
        definition.addDef("loan",False)

        #TODO
        #create DGH for default
        defaultDGH = DGHFactory.createCreditDefault()
        definition.addDef("default",False,defaultDGH)

        result = DataSet(file,definition)
        return result
