from DHGTreeNode import DHGTreeNode
 
class DHG:

    def __init__(self):
        self.root = DHGTreeNode("Any", self)

    def addValue(self, value, parent):

        if (not parent in self.root.children and not parent == "Any"):
            return False

        search_node = self.root
        while (True):

            search_node.addChild(value)

            if (search_node.value == parent):
                search_node.addLeaf(value)
                return True
            else:
                for child in search_node.pointers:
                    if (child.value == parent or (parent in child.children)):
                        search_node = child
                        break

    def getLCA(self, val_1, val_2):

        if ((not val_1 in self.root.children) or (not val_2 in self.root.children)):
            return "A value provided is not in the tree"

        search_node = self.root
        while (True):


            for child in search_node.pointers:
                if (val_1 in child.children and val_2 in child.children):
                    search_node = child
                    break

            return search_node.value
        
    def countLeaves(self):

        return self.root.countNodeLeaves()

    
    def getLeftTraversal(self) -> list(DHGTreeNode):
        return self.root.traverseLeft()
    
    def getRoot(self):
        return self.root
