from heapq import heapify
import heapq
from http.client import UnimplementedFileMode
from random import random
import string
from Attribute import Attribute
from DataSet import DataSet

from cluster import Cluster
from heap_node import HeapNode
from my_heap import MyHeap
from Attribute import Attribute
from typing import Tuple , List ,  Dict
from tupleWrapper import TupleWrapper


class CASTLE:

    #declaring contants
    #what form of k-anonymity are we using
    K:int =3
    #maximum time between a tuple is received and the tuple is outputed
    DELTA:int = 1
    #maximum number of non k-anonymized clusters that we can store
    BETA:int = 5

    mu:int = 5

    #average infoLoss of the mu more recent k anonymized clusters
    tau:int = 0

    recentClusters:List[Cluster] = []

    #Dictionary where the key is the index
    allTuples: Dict[int,TupleWrapper] = {}

    #the index of the next tuple to be read
    nextTupleIndex:int = 0

    #class variables
    # set of non k_s anonymized clusters
    gamma:List[Cluster] = []
    
    # set of k_s anonymized clusters
    omega:List[Cluster] = [] 

    myAttributes:List[Attribute] = []

    def __init__(self, ds: DataSet):
        self.ds: DataSet = ds

    #tuple is the new row read from the stream
    #return a list of tuples 
    def readTuple(self,tuple:Tuple) -> List[Tuple]:
        newTuple:TupleWrapper = self.createWrapper(tuple)
        C = self.best_selection(newTuple, self.gamma)
        if C is None:
            self.gamma.append(self.createCluster(newTuple))
        else:
            C.add_to_cluster(newTuple)
        return self.getOutput()

    def createWrapper(self,t:Tuple) -> TupleWrapper:
        result = TupleWrapper(t,self.nextTupleIndex)
        self.allTuples[self.nextTupleIndex] = result
        self.nextTupleIndex= self.nextTupleIndex+1
        return result


    #TODO
    def getOutput(self) ->List[Tuple]:
        staleTupleIndex = self.nextTupleIndex-1-self.DELTA
        staleTuple = self.allTuples[staleTupleIndex]
        self.allTuples[staleTupleIndex] = None
        if (staleTuple is None):
            return []
        else:
            return self.delay_constraint(staleTuple)

    #returns a string tuple
    #
    #A tuple is going to expire
    def delay_constraint(self,staleTuple:TupleWrapper)->List[Tuple]:
        #cluster is the cluster in gamme containing tuple
        cluster:Cluster = staleTuple.getCluster()
        if (cluster.size()>self.K):
            return self.outputCluster(cluster)
        
        #clusters in omega containing tuple
        clusters:List[Cluster] = staleTuple.getKAnonCluster()
        if (len(clusters)>0):
            return [random.choice(clusters).get_generic(staleTuple)]

        m:int =0
        mergeSize:int = 0
        otherClusters:List[Cluster] = []  #clusters in gamma that is not cluster
        for c in self.gamma:
            mergeSize += c.size()
            if(cluster.size()<c.size()):
                if (cluster != c):
                    otherClusters.append(c)
                m+=1

        if (m>len(self.gamma)/2):
            return [self.suppress(staleTuple)]
        
        if (mergeSize<self.K):
            return [self.suppress(staleTuple)]

        mergedCluster = self.mergeClusters(cluster,otherClusters)
        return self.outputCluster(mergedCluster)


    def mergeClusters(self, c: Cluster, clusters: list(Cluster))->Cluster:
        merged= {}
        for cluster in clusters:
            merged[cluster] = self.calc_enlargement(c,cluster)
        
        minCluster = min(merged,key=merged.get)
        c.enlarge(minCluster)
 
        if (c.size()>=self.K):
            return c
        clusters.remove(minCluster)
        return self.mergeClusters(c,clusters)
    
    # info loss score for adding c1 to c2
    def calc_enlargement(self, c1: Cluster, c2: Cluster):
        new_ranges = {}
        sum_info_loss = 0
        attributes = c2.ds.getAttributes
        for attr_pos in range(len(attributes)): #this could change to be myAttributes instead?
            attr: Attribute = attributes[attr_pos]
            range = []
            for tuple in c1.tuples:
                if attr.isQI:
                    range = attr.expandRange(c2.ranges[attr], tuple[attr_pos])
            new_ranges[attr] = range
            sum_info_loss += attr.calculateInfoLoss(range)
        return sum_info_loss

    #return the maximum generalization for each QI
    def suppress(self,tuple: TupleWrapper):
        result = []
        for a in self.myAttributes:
            if (a.isQI()):
                result.append(a.getGeneralization())
            else:
                result.append(a.getValue(tuple))
        return Tuple(result)


    def getGammaCluster(self,tuple:TupleWrapper):
        return NotImplementedError
    def getOmegaCluster(self,tuple:TupleWrapper):
        return NotImplementedError

    def recalculateTau(self,newCluster: Cluster):
        #get the mu most recent cluster
        num = len(self.recentClusters)
        if (num<self.mu):
            self.tau = ((self.tau*num)+newCluster.get_info_loss()) / (num+1)
        else:
            popped = self.recentClusters.pop(0)
            self.tau = ((self.tau*self.mu)-popped.get_info_loss()+newCluster.get_info_loss()) / self.mu

        self.recentClusters.append(newCluster)

    #where cluster is the cluster to be outputted
    def outputCluster(self, cluster:Cluster) -> List[Tuple]:
        clusters:List[Cluster] = [cluster]

        #we split the cluster when suitable
        if (cluster.size()>=2*self.K):
            clusters = self.split(cluster)

        result:List[Tuple] = []
        for c in clusters:
            result.extend(c.output_cluster())
            t: TupleWrapper
            for t in c.tuples:
                self.allTuples[t.getIndex()] = None

            self.recalculateTau(c)
            if (c.get_info_loss()<self.tau):
                self.omega.append(c)
           # else:
                #delete C???
            #    return NotImplementedError
            self.gamma.remove(c)
        return result


    def createCluster(self,t:TupleWrapper)->Cluster:
        cluster: Cluster = Cluster(self.ds)
        cluster.add_to_cluster(t)
        return cluster
    
    #return the cluster from set of given clusters whose enlargement results in the smallest information loss
    def best_selection(self,t:TupleWrapper,candidate_clusters:List[Cluster]) -> Cluster: 
        changeInInfoLoss:Dict[Cluster,float] = {}
        infoLoss:Dict[Cluster,float] = {}
        for cluster in candidate_clusters:
            infoLoss[cluster] = cluster.get_info_loss(t)
            changeInInfoLoss[cluster] = infoLoss[cluster]-cluster.get_info_loss()
        minValue = min(changeInInfoLoss.itervalues())
        minClusters:List[Cluster] = [k for k, v in changeInInfoLoss.iteritems() if v == minValue]
                
        SetCok:List[Cluster]=[]
        for cluster in minClusters:
            if (infoLoss[cluster]<=self.tau):
                SetCok.append(cluster)

        if len(SetCok) == 0:
            if (len(self.gamma)>=self.BETA):
                return random.choice(minClusters)
            else:
                return None
        else:
            return random.choice(SetCok)


    def split(self, C: Cluster):
        sc = list()
        # let BS be the buckets created by grouping tuples in C by pid attribute
        bs: list(list(tuple)) = C.get_buckets
        while len(bs) >= self.K:
            Bbar: list(tuple) = random.choice(bs)
            tbar: tuple = random.choice(Bbar)
            Bbar.remove(tbar)               # assuming this step is required
            # create a new sub-cluster Cnew over tbar 
            Cnew: Cluster = Cluster(C.ds)
            Cnew.add_to_cluster(tbar)
            if len(Bbar) == 0:
                bs.remove(Bbar)
            heap = MyHeap(self.K)
            # red_bs is BS\Bbar
            red_bs: list() = bs.copy()
            if Bbar in red_bs:
                red_bs.remove(Bbar)
            for bucket in red_bs:
                t: tuple = bucket[0]
                t_dist = self.calc_distance(tbar, t)
                heap_node: HeapNode = HeapNode(t, t_dist)
                # if t is closer to tbar than the root of H_(k-1):
                    # t replaces the root, and H_(k-1) is adjusted accordingly
                heap.add_to_heap(heap_node)
            node: HeapNode
            for node in heap.my_heap:
                tbar: tuple = node.get_tuple
                Cnew.add_to_cluster(tbar)
                # Let B_j be the bucket containing tbar
                for B_j in red_bs:
                    if tbar in B_j:
                        B_j.remove(tbar)
                        if len(B_j) == 0:
                            red_bs.remove(B_j)
                        break
            sc.append(Cnew)
        for B_i in bs:
            t_i = random.choice(B_i)
            nearest_cluster: Cluster = self.best_selection(t_i, sc)
            for t in B_i:
                nearest_cluster.add_to_cluster(t)
            bs.remove(B_i)
        return sc

    #TODO
    # return the distance between the two tuples
    def calc_distance(self, tbar, t):
        return NotImplementedError
