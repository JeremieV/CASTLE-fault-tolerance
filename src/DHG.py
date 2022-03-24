from DHGTreeNode import DHGTreeNode
from typing import List
 
class DHG:

    #def __init__(self):
     #   self.root = DHGTreeNode("Any", self)

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

    
    def getLeftTraversal(self) -> List[DHGTreeNode]:
        return self.root.traverseLeft()
    
    def getRoot(self):
        return self.root
