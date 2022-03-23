class DHGTreeNode:

    def __init__(self, value, parent):
        
        self.parent = parent
        self.value = value
        self.children: list(DHGTreeNode) = []
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
        child: DHGTreeNode
        for child in self.pointers:
            count = count + child.countNodeLeaves()
        return count
    
    def traverseLeft(self):
        traversed_nodes: list(DHGTreeNode) = []
        halfway: int = len(self.children)//2
        for i in range(halfway):
            child: DHGTreeNode = self.children[i]
            traversed_nodes.append(child.traverseLeft())
        traversed_nodes.append(self)
        for i in range((halfway+1), len(self.children)):
            child: DHGTreeNode = self.children[i]
            traversed_nodes.append(child.traverseLeft())
        return traversed_nodes

            