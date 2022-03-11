from random import random

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
    # set of k_s anonymized clusters
    gamma = []
    # set of non k_s anonymized clusters
    omega = [] 

    #tuple is the new row read from the stream
    def readTuple(self,tuple,delta):

        C = self.best_selection(tuple)
        if C is None:
            self.gamma.add(self.createCluster(tuple))
        else:
            C.add(tuple)
        t_prime = tuple.p - delta # ??
        # if t_prime has not yet been output:
        #     delay_constraint(t_prime)
    
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
    
    #return the cluster whose enlargement results in the smallest information loss
    def best_selection(self,t): 
        minEnlargement=0
        minClusters = {}
        for cluster in self.gamma:
            enlargedLoss = CASTLE.getInfoLoss(cluster, t)
            val = enlargedLoss-cluster.getInfoLoss()

            if (val<minEnlargement):
                minEnlargement=val
                minClusters = {}

            if (val==minEnlargement): 
                minClusters[cluster] = enlargedLoss
                
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