class DHGTreeNode:

    def __init__(self, value, parent):
        
        self.parent = parent
        self.value = value
        self.children = []
        self.pointers = []

    def isLeaf(self):
        if (len(self.pointers) == 0):
            return True
        else:
            return False

    def addChild(self, value):
        self.children.append(value)

    def addLeaf(self, value):
        self.pointers.append(DHGTreeNode(value, self))

    def countNodeLeaves(self):

        if (self.isLeaf()):
            return 1

        count = 0
        for child in self.pointers:
            count = count + child.countNodeLeaves()
        return count