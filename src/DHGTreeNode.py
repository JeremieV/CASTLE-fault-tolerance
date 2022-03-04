class DHGTreeNode:

    def __init__(self, name, values, parent):
        self.values = values
        self.parent = parent
        self.name = name
        self.pointers = []

    def addLeaf(self, name, values):
        self.pointers.append(DHGTreeNode(name, values, self))




    