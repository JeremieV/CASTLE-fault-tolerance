from heapq import heapify
import heapq
from http.client import UnimplementedFileMode
from math import sqrt, gamma
import random
import statistics
import string
import heapq
from unittest import result
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
    DELTA:int = 10
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
        self.myAttributes:List[Attribute] = ds.getAttributes()
        for a in self.myAttributes:
            if (a.isPID()):
                self.myPID = a

    #tuple is the new row read from the stream
    #return a list of tuples 
    def readTuple(self,tuple:Tuple) -> List[Tuple]:
        invalid =False
        for val in tuple:
            if val =="":
                invalid=True
        if (invalid==False): 
            newTuple:TupleWrapper = self.createWrapper(tuple)
            C = None
            if len(self.gamma) > 0:
                C = self.best_selection(newTuple, self.gamma)
            if C is None:
                self.gamma.append(self.createCluster(newTuple))
            else:
                C.add_to_cluster(newTuple)
            return self.getOutput()
        return []

    def createWrapper(self,t:Tuple) -> TupleWrapper:
        result = TupleWrapper(t,self.nextTupleIndex)
        self.allTuples[self.nextTupleIndex] = result
        self.nextTupleIndex= self.nextTupleIndex+1
        return result

    def getOutput(self) ->List[Tuple]:
        staleTupleIndex = self.nextTupleIndex-1-self.DELTA
        staleTuple = None
        if staleTupleIndex >= 0:
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
        cluster:Cluster = self.getGammaCluster(staleTuple)
        if (len(cluster)>self.K):
            return self.outputCluster(cluster)
        
        #clusters in omega containing tuple
        clusters:List[Cluster] = self.getOmegaCluster(staleTuple)
        if (len(clusters)>0):
            return [random.choice(clusters).get_generic(staleTuple)]

        m:int =0
        mergeSize:int = 0
        otherClusters:List[Cluster] = []  #clusters in gamma that is not cluster
        for c in self.gamma:
            mergeSize += len(c)
            if(len(cluster)<len(c)):
                m+=1
            if (c!=cluster):
                otherClusters.append(c)

        if (m>len(self.gamma)/2):
            return [self.suppress(staleTuple)]
        
        if (mergeSize<self.K):
            return [self.suppress(staleTuple)]

        mergedCluster = self.mergeClusters(cluster,otherClusters)
        return self.outputCluster(mergedCluster)


    def mergeClusters(self, c: Cluster, clusters: List[Cluster])->Cluster:
        merged= {}
        if len(clusters) == 0:
            return None
        for cluster in clusters:
            merged[cluster] = self.calc_enlargement(c,cluster)
        
        minCluster = min(merged,key=merged.get)
        c.enlarge(minCluster)
 
        if (len(c)>=self.K):
            return c
        # self.gamma.remove(minCluster)
        clusters.remove(minCluster)
        return self.mergeClusters(c,clusters)
    
    # info loss score for adding c1 to c2
    def calc_enlargement(self, c1: Cluster, c2: Cluster):
        new_ranges = {}
        sum_info_loss = 0
        attributes = self.myAttributes
        for attr_pos in range(len(attributes)): #this could change to be myAttributes instead?
            attr: Attribute = attributes[attr_pos]
            new_range = []
            for tuple in c1.tuples:
                if attr.isQI:
                    new_range = attr.expandRange(c2.ranges[attr], tuple.getTuple()[attr_pos])
            new_ranges[attr] = new_range
            sum_info_loss += attr.calculateInfoLoss(new_range)
        return sum_info_loss

    #return the maximum generalization for each QI
    def suppress(self,t: TupleWrapper):
        result = []
        for a in self.myAttributes:
            if (a.isQI()):
                result.append(a.getGeneralization())
            else:
                result.append(a.getValue(t))
        return tuple(result)


    def getGammaCluster(self,tuple:TupleWrapper)->Cluster:
        for c in self.gamma:
            if (c.contains(tuple)):
                return c

    def getOmegaCluster(self,tuple:TupleWrapper):
        result:List[Cluster] = []
        for c in self.omega:
            if (c.contains(tuple)):
                result.append(c)
        return result

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
        if cluster is None:
            pass
        clusters:List[Cluster] = [cluster]

        #we split the cluster when suitable
        if (len(cluster)>=2*self.K):
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
        minValue = min(changeInInfoLoss.values())
        minClusters:List[Cluster] = [k for k, v in changeInInfoLoss.items() if v == minValue]
                
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
        results:List[Cluster] = []
        # let BS be the buckets created by grouping tuples in C by pid attribute
        buckets: Dict[str,List[TupleWrapper]] = {}
      #  bs: list(list(tuple)) = C.get_buckets()
        while len(buckets) >= self.K:
            selectedBucket:List[TupleWrapper] = random.choice(buckets.values())
            selectedTuple:TupleWrapper = random.choice(selectedBucket)
                
            #create a new cluster over selectedTuple
            # create a new sub-cluster Cnew over tbar 
            Cnew: Cluster = Cluster(C.ds)
            Cnew.add_to_cluster(selectedTuple)

            myQueue = []
            for bucket in buckets.values():
                if bucket == selectedBucket:
                    continue
                if (len(bucket) == 0):
                    buckets.remove(bucket)
                    continue
                distance:float = self.calc_distance(bucket[0],selectedTuple)
                if (len(myQueue)>=self.K-1):
                    if (min(myQueue)[0]<=distance):
                        continue
                    heapq.heappop(myQueue)
                heapq.heappush(myQueue,(distance,bucket[0]))

            for pair in myQueue:
                currentTuple:TupleWrapper = pair[1]
                Cnew.add_to_cluster(currentTuple)
                pid = self.myPID.getValue(currentTuple)
                currentBucket =  buckets[pid]
                currentBucket.remove(currentTuple)
                if (len(currentBucket)==0):
                    buckets.remove(currentBucket)
            results.append(Cnew)

        for bucket in buckets.values():
            if (len(bucket) != 0):
                myTuple:TupleWrapper = random.choice(bucket)
                minChange = -1
                nearestCluster = results[0]
                for c in results:
                    change:int = c.get_info_loss(myTuple)-c.get_info_loss()
                    if (minChange==-1 or change<minChange):
                        minChange=change
                        nearestCluster=c
                
                #find the nearest cluster in result
                for currentTuple in bucket:
                    nearestCluster.add_to_cluster(currentTuple)
            buckets.remove(bucket)
        return results

    # return the distance between the two tuples
    def calc_distance(self, tbar, t):
        distances: List(float) = []
        for i in range(len(self.myAttributes)):
            attr: Attribute = self.myAttributes[i]
            distances.append(attr.calc_distance(tbar, t))
        mean_distance =  sqrt(statistics.mean(distances))
        return mean_distance
