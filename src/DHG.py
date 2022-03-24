from DHGTreeNode import DHGTreeNode
from typing import List
 
class DHG:

    def getLCA(self, val_1, val_2):
        leaf = self.leaves[val_1]        
        return leaf.getLCA(val_1, val_2)

        
    def countLeaves(self):
        return self.root.countNodeLeaves()

    
    def getLeftTraversal(self) -> List[DHGTreeNode]:
        return self.root.traverseLeft()
    
    def getRoot(self):
        return self.root
