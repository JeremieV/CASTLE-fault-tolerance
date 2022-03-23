from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

class DHGTreeNode(object):


    def __init__(self, value, parent=None):
        self.index:int = 0 #refers to the node's position in the tree
        self.parent:DHGTreeNode = None
        self.value:str = value  
        self.children: List[DHGTreeNode] = []

    def addChild(self, child:DHGTreeNode):
        self.children.append(child)

    def isLeaf(self):
        if (len(self.children) == 0):
            return True
        else:
            return False

    def countNodeLeaves(self):

        if (self.isLeaf()):
            return 1

        count = 0
        child: DHGTreeNode
        for child in self.children:
            count = count + child.countNodeLeaves()
        return count
    
    def traverseLeft(self) ->List:
        traversed_nodes: List[DHGTreeNode] = []
        halfway: int = len(self.children)//2
        
        for i in range(halfway):
            child: DHGTreeNode = self.children[i]
            traversed_nodes.append(child.traverseLeft())

        traversed_nodes.append(self)
        for i in range((halfway+1), len(self.children)):
            child: DHGTreeNode = self.children[i]
            traversed_nodes.append(child.traverseLeft())
        return traversed_nodes

            