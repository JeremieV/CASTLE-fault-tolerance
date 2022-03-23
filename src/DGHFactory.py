from DHG import DHG
from DHGTreeNode import DHGTreeNode

#hard code the creation of the DGH
class DGHFactory:

    def __init__(self):
        self.credit_tree_default = None

    # Creates a discrete DHG and generalises both 0 and 1 to 'maybe'
    def _createTreeDefault(self):
        self.credit_tree_default = DHG()
        maybe = DHGTreeNode("Maybe")
        yes = DHGTreeNode("1")
        no = DHGTreeNode("0")
        no.parent=maybe
        yes.parent = maybe
        maybe.children.append(no)
        maybe.children.append(yes)



    # Generalise both possible results into maybe
    def _addDefault(self, value, parent):
        self.credit_tree_default.addValue(value, parent)

    # Returns a DHG for the default values of the credit_data.csv file
    def createCreditDefault(self):
        self._createTreeDefault()
        return self.credit_tree_default