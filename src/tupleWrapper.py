from typing import List, Tuple
from cluster import Cluster

class TupleWrapper(object):

    def __init__(self,myTuple:Tuple,index:int) -> None:
        self.Content = myTuple
        self.index = index

    def getIndex(self) -> int:
        return self.index

    def getTuple(self) -> Tuple:
        return self.Content

    #return a list of k anomlyized clusters which contain the tuple
    def getKAnonCluster(self)->List[Cluster]:
        #TODO
        return []

    #return the non K-anomlyized clusters which contain the tuple
    def getCluster(self)->Cluster:
        #TODO
        return None
