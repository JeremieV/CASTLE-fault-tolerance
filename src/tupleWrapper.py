from typing import Tuple


class TupleWrapper:

    def __init__(self,myTuple:Tuple,index:int) -> None:
        self.Content = myTuple
        self.index = index

    def getIndex(self) -> int:
        return self.index
