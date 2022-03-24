from operator import contains
from DHGTreeNode import DHGTreeNode
from typing import List
 
class DHG:

    root: DHGTreeNode

    #def __init__(self):
     #   self.root = DHGTreeNode("Any", self)

    def getLCA(self, val_1, val_2):
        node_1 = self.getRoot().findNode(val_1)
        search_node: DHGTreeNode = node_1
        while(True):
            if search_node.containsValue(val_2):
                return search_node.value
            else:
                if search_node is self.root:
                    return "A value provided is not in the tree"
                search_node = search_node.parent


        
    def countLeaves(self):
        return self.root.countNodeLeaves()

    
    def getLeftTraversal(self) -> List[DHGTreeNode]:
        return self.root.traverseLeft()
    
    def getRoot(self) -> DHGTreeNode:
        return self.root
    
    def addValue(self, value, parent):

        if (not parent in self.root.children and not parent == "Any"):
            return False

        search_node: DHGTreeNode = self.root
        while (True):

            search_node.addChild(value)

            if (search_node.value == parent.value):
                search_node.addLeaf(value)
                return True
            else:
                for child in search_node.children:
                    if (child.value == parent.value or (parent in child.children)):
                        search_node = child
                        break
