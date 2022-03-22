from heapq import heapify
import heapq
from http.client import UnimplementedFileMode
from random import random

from cluster import Cluster
from heap_node import HeapNode
from my_heap import MyHeap

class CASTLE:

    #declaring contants
    #what form of k-anonymity are we using
    K=3
    #maximum time between a tuple is received and the tuple is outputed
    DELTA = 1
    #maximum number of non k-anonymized clusters that we can store
    BETA = 5

    tau = 0

    #class variables
    # set of non k_s anonymized clusters
    gamma = []
    
    # set of k_s anonymized clusters
    omega = [] 

    #tuple is the new row read from the stream
    def readTuple(self,tuple,time):

        C = self.best_selection(tuple, self.gamma)
        if C is None:
            self.gamma.add(self.createCluster(tuple))
        else:
            C.add(tuple)

        return self.getOutput(time)

    #TODO
    #return the time that the tuple was received from the data stream
    def getTimeReceived(self,tuple):
        return NotImplementedError

    #TODO
    #return an list of tuples that needs to be outputted
    def __getStaleTuples(self,time):
        t_prime = time - self.DELTA
        return NotImplementedError

    #TODO
    def getOutput(self,time):
        tuples = self.__getStaleTuples(time)

        if (len(tuples)==0):
            return []
        else:
            pass
           # self.delay_constraint(t_prime)
            return NotImplementedError

    #returns a string
    def delay_constraint(self,tuple):
        #cluster is the cluster in omega containing tuple
        cluster = None
        if (cluster.size()>self.K):
            return self.outputCluster(cluster)
        
        #clusters in gamma containing tuple
        clusters = []
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
            return self.suppress(tuple)
        
        if (mergeSize<self.K):
            return self.suppress(tuple)

        mergedCluster = self.mergeClusters(cluster,otherClusters)
        return self.outputCluster(mergedCluster)


    def mergeClusters(self,c,clusters):
        merged= {}
        for cluster in clusters:
            merged[cluster] = calcEnlargement(c,cluster)
        
        minCluster = min(merged,key=merged.get)
        c.enlarge(minCluster)
 
        if (c.size()>=self.K):
            return c
        clusters.remove(minCluster)
        return self.mergeClusters(c,clusters)

    #TODO
    #return the maximum generalization for each QI
    def suppress(self,tuple):
        return NotImplementedError

    def recalculateTau(self,cluster):
        return NotImplementedError

    def outputCluster(self, cluster):
        clusters = [cluster]
        if (cluster.size()>=2*self.K):
            clusters = cluster.split()

        result = ""
        for c in clusters:
            result += c.output()
            self.recalculateTau(c)

            if (self.getInfoLoss(c)<self.tau):
                self.omega.append(c)
            else:
                #delete C???
                return NotImplementedError
            self.gamma.remove(c)

    
    #TODO
    #return the information loss of a cluster
    #if a tuple is supplied, then return the info loss of the enlarged cluster
    def getInfoLoss(cluster,tuple=None):
        if (tuple==None):
            return cluster.getInfoLoss()
        else:
            #enlarge
            pass


    #TODO
    def createCluster(self,tuple):
        return NotImplementedError
    
    #return the cluster from set of given clusters whose enlargement results in the smallest information loss
    def best_selection(self,t,candidate_clusters): 
        clusters = {}
        infoLoss = {}
        for cluster in candidate_clusters:
            infoLoss[cluster] = CASTLE.getInfoLoss(cluster, t)
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
