from heapq import heapify
import heapq
from http.client import UnimplementedFileMode
from random import random
from Attribute import Attribute

from cluster import Cluster
from heap_node import HeapNode
from my_heap import MyHeap
from Attribute import Attribute
from typing import Tuple,List
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
    allTuples = {}

    #the index of the next tuple to be read
    nextTupleIndex:int = 0

    #class variables
    # set of non k_s anonymized clusters
    gamma:List[Cluster] = []
    
    # set of k_s anonymized clusters
    omega:List[Cluster] = [] 

    myAttributes:List[Attribute] = []

    #tuple is the new row read from the stream
    #return a list of tuples 
    def readTuple(self,tuple:Tuple):
        newTuple:TupleWrapper = self.createWrapper(tuple)
        C = self.best_selection(newTuple, self.gamma)
        if C is None:
            self.gamma.add(self.createCluster(newTuple))
        else:
            C.add(newTuple)
        return self.getOutput()

    def createWrapper(self,t:Tuple) -> TupleWrapper:
        result = TupleWrapper(t,self.nextTupleIndex)
        self.allTuples[self.nextTupleIndex] = result
        self.nextTupleIndex= self.nextTupleIndex+1
        return result


    #TODO
    def getOutput(self):
        staleTupleIndex = self.nextTupleIndex-1-self.DELTA
        staleTuple = self.allTuples[staleTupleIndex]
        if (staleTuple is None):
            return ()
        else:
            self.delay_constraint(staleTuple)

    #returns a string tuple
    #
    #A tuple is going to expire
    def delay_constraint(self,staleTuple:TupleWrapper):
        #cluster is the cluster in gamme containing tuple
        cluster = staleTuple.getCluster()
        if (cluster.size()>self.K):
            return self.outputCluster(cluster)
        
        #clusters in omega containing tuple
        clusters = staleTuple.getKAnonCluster()
        if (len(clusters)>0):
            return random.choice(clusters)
        
        m=0
        mergeSize = 0
        otherClusters = []  #clusters in gamma that is not cluster
        for c in self.gamma:
            mergeSize += c.size()
            if(cluster.size()<c.size()):
                if (cluster != c):
                    otherClusters.append(c)
                m+=1

        if (m>len(self.gamma)/2):
            return self.suppress(staleTuple)
        
        if (mergeSize<self.K):
            return self.suppress(staleTuple)

        mergedCluster = self.mergeClusters(cluster,otherClusters)
        return self.outputCluster(mergedCluster)


    def mergeClusters(self,c,clusters):
        merged= {}
        for cluster in clusters:
            merged[cluster] = self.getEnlargedInfoLoss(c,cluster)
        
        minCluster = min(merged,key=merged.get)
        c.enlarge(minCluster)
 
        if (c.size()>=self.K):
            return c
        clusters.remove(minCluster)
        return self.mergeClusters(c,clusters)

    #TODO
    #return the maximum generalization for each QI
    def suppress(self,tuple: TupleWrapper):
        result = []
        for a in self.myAttributes:
            if (a.isQI()):
                result.append(a.getGeneralization())
            else:
                result.append(a.getValue(tuple))
        return Tuple(result)

    def recalculateTau(self,newCluster: Cluster):
        #get the mu most recent cluster
        num = len(self.recentClusters)
        if (num<self.mu):
            self.tau = ((self.tau*num)+newCluster.getInfoLoss()) / (num+1)
        else:
            popped = self.recentClusters.pop(0)
            self.tau = ((self.tau*self.mu)-popped.getInfoLoss()+newCluster.getInfoLoss()) / self.mu

        self.recentClusters.append(newCluster)

    def outputCluster(self, cluster):
        clusters = [cluster]
        if (cluster.size()>=2*self.K):
            clusters = cluster.split()

        result = ""
        for c in clusters:
            result += c.output()
            self.recalculateTau(c)

            if (self.getEnlargedInfoLoss(c)<self.tau):
                self.omega.append(c)
            else:
                #delete C???
                return NotImplementedError
            self.gamma.remove(c)

    
    #return the information loss of a cluster
    #if a tuple is supplied, then return the info loss of the enlarged cluster
    def getEnlargedInfoLoss(self,cluster: Cluster,tuple:TupleWrapper=None) -> float:
        if (tuple==None):
            return cluster.get_info_loss()
        else:
            sum_info_loss:float = 0
            n:int = 0

            for attribute in self.myAttributes:
                if (attribute.isQI()):
                    newRange = attribute.expandRange(cluster.ranges[attribute],attribute.getValue(tuple))
                    sum_info_loss += attribute.calculateInfoLoss(newRange)
                    n += 1
            return sum_info_loss/n


    #TODO
    def createCluster(self,tuple:TupleWrapper)->Cluster:
        return NotImplementedError
    
    #return the cluster from set of given clusters whose enlargement results in the smallest information loss
    def best_selection(self,t:TupleWrapper,candidate_clusters:List[Cluster]): 
        clusters = {}
        infoLoss = {}
        for cluster in candidate_clusters:
            infoLoss[cluster] = self.getInfoLoss(cluster, t)
            val = infoLoss[cluster]-cluster.getInfoLoss()
            clusters[cluster] = val
        minValue = min(clusters.itervalues())
        minClusters = [k for k, v in clusters.iteritems() if v == minValue]
                
        SetCok=[]
        for cluster in minClusters:
            if (minClusters[cluster]<=self.tau):
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
