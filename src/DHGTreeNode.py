class DHGTreeNode:

    def __init__(self, params, parent, discrete):
        
        self.parent = params[0]
        self.discrete = discrete
        self.values = []

        if (discrete):
            self.name = params[0]
            self.addValue(params[1])
        else:
            self.name = params[0] + " - " + params[1]
            self.range = [params[0], params[1]]

        self.pointers = []

    def addValue(self, value):
        self.values.append(value)

    def addLeaf(self, params):
            self.pointers.append(DHGTreeNode(params, self, self.discrete))
            
    def getRange(self):
        return (self.range[1] - self.range[0])




    