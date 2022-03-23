from typing import List, Tuple

class TupleWrapper(object):

    def __init__(self,myTuple:Tuple,index:int) -> None:
        self.Content = myTuple
        self.index = index

    def getIndex(self) -> int:
        return self.index

    def getTuple(self) -> Tuple:
        return self.Content
