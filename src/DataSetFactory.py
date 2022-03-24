from DGHFactory import DGHFactory
from DataSet import DataSet

#describes information about a column 
#used in DataSet initialization
class ColumnDefinition:
    #dictionary to store if a column is a QI
    QIMap = {}
    #dictionary to store the DHG of a column
    DGHMap = {}

    PIDName = ""

    def addDef(self,columnName,QI,DGH=None):
        self.QIMap[columnName] = QI
        if (DGH!=None):
            self.DGHMap[columnName] = DGH

    def isQI(self,columnName):
        if (columnName in self.QIMap.keys()):
            return self.QIMap[columnName]
        return False

    def isPID(self,columnName):
        return columnName==self.PIDName

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
        definition.PIDName = "clientid"

        # I'm not great at python so calling the factory class like this
        fac = DGHFactory()
        defaultDGH = fac.createCreditDefault()
        definition.addDef("default",True,defaultDGH)

        result = DataSet(file,definition)
        return result