from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

class DHGTreeNode(object):


    def __init__(self, value, parent=None):
        self.index:int = 0 #refers to the node's position in the tree
        self.parent:DHGTreeNode = None
        if not parent is None:
            self.parent = parent
        self.value:str = value  
        self.children: List[DHGTreeNode] = []

    def addChild(self, child:DHGTreeNode):
        self.children.append(child)

    def isLeaf(self):
        if (len(self.children) == 0):
            return True
        else:
            return False
    
    def addLeaf(self, value):
        self.children.append(DHGTreeNode(value, self))
    
    def containsValue(self, val:str):
        if self.value == val:
            return True
        for child in self.children:
            if child.containsValue(val):
                return True
        return False
    
    def findNode(self, val:str):
        if self.value == val:
            return self
        for child in self.children:
            end_node = child.findNode(val)
            if not end_node is None:
                return end_node
        return None

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
            traversed_nodes.extend(child.traverseLeft())

        traversed_nodes.append(self)
        for i in range((halfway+1), len(self.children)):
            child: DHGTreeNode = self.children[i]
            traversed_nodes.extend(child.traverseLeft())
        return traversed_nodes

            