from DHG import DHG

#hard code the creation of the DGH
class DGHFactory:

    def __init__(self):
        self.credit_tree_default = None

    # Creates a discrete DHG and generalises both 0 and 1 to 'maybe'
    def _createTreeDefault(self):
        self.credit_tree_default = DHG()
        self._addDefault("Maybe", "Any")
        self._addDefault("1", "Maybe")
        self._addDefault("0", "Maybe")

    def _createTreeIncome(self):
        self.credit_tree_income = DHG(False)
        self._addIncome(0, 19999)
        self._addIncome(20000, 39999)
        self._addIncome(40000, 59999)
        self._addIncome(60000, 79999)
        self._addIncome(80000, 99999)
        self._addIncome(100000, 150000)

    def _createTreeAge(self):
        self.credit_tree_age = DHG(False)
        self._addAge(18, 30)
        self._addAge(31, 45)
        self._addAge(46, 60)
        self._addAge(61, 80)
        self._addAge(81, 100)

    def _createTreeLoan(self):
        self.credit_tree_loan = DHG(False)
        self._addIncome(0, 1999)
        self._addIncome(2000, 3999)
        self._addIncome(6000, 7999)
        self._addIncome(8000, 9999)
        self._addIncome(10000, 15000)

    def _addIncome(self, min, max):
        self.credit_tree_income.buildContinuousLeaf(min, max)
        
    def _addAge(self, min, max):
        self.credit_tree_age.buildContinuousLeaf(min, max)

    def _addLoan(self, min, max):
        self.credit_tree_loan.buildContinuousLeaf(min, max)

    # Generalise both possible results into maybe
    def _addDefault(self, value, parent):
        self.credit_tree_default.addValue(value, parent)

    # Returns a DHG for the default values of the credit_data.csv file
    def createCreditDefault(self):
        self._createTreeDefault()
        return self.credit_tree_default