
class CASTLE:

    #declaring contants
    #what form of k-anonymity are we using
    K=3
    #maximum time between a tuple is received and the tuple is outputed
    DELTA = 1
    #maximum number of non k-anonymized clusters that we can store
    BETA = 5

    #class variables
    # set of k_s anonymized clusters
    gamma = []
    # set of non k_s anonymized clusters
    omega = [] 

    #tuple is the new row read from the stream
    def readTuple(self,tuple,delta):
        tau = 0

        C = self.best_selection(tuple)
        if C is None:
            self.gamma.add(self.createCluster(tuple))
        else:
            C.add(tuple)
        t_prime = tuple.p - delta # ??
        # if t_prime has not yet been output:
        #     delay_constraint(t_prime)

    #TODO
    def createCluster(self,tuple):
        return NotImplementedError
    
    #return the cluster whose enlargement results in the smallest information loss
    def best_selection(self,t): 
        E = set()
        for C_j in self.gamma:
            e = Enlargement(C_j, t)
            E.add(e)
        _min_ = min(E)

        SetCMin = {c for c in self.gamma if Enlargement(c, t) == _min_}
        SetCok=[]
        for C_j in SetCMin:
            #info_loss is the information loss of c_j after enlargement
            #TODO
            info_loss = None
            if (info_loss<=self.tau):
                SetCok.append(C_j)

        if len(SetCok) == 0:
            if (len(self.gamma)>=self.BETA):
                #result = any cluster is setC<om with the minimum size
                return result
            else:
                return None
        else:
            #result = a cluster in SetCMin with minimum size
            return result