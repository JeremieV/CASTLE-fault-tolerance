from DHGTreeNode import DHGTreeNode
from typing import List
 
class DHG:

    #def __init__(self):
     #   self.root = DHGTreeNode("Any", self)

    def getLCA(self, val_1, val_2):
        i = self.leaveContents.index(val_1)
        i2 = self.leaveContents.index(val_2)
        leaf = self.leaves[i]
        
        return leaf.getLCA(i, i2)
       # if ((not val_1 in self.root.children) or (not val_2 in self.root.children)):
        #    return "A value provided is not in the tree"

        
        
    def countLeaves(self):
        return self.root.countNodeLeaves()

    
    def getLeftTraversal(self) -> List[DHGTreeNode]:
        return self.root.traverseLeft()
    
    def getRoot(self):
        return self.root
