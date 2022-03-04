import csv
import asyncio
import random

from cluster import Cluster
from Attribute import Attribute
from DataSet import DataSet

# The parameters that affect the performance of CASTLE are: delta, k, the number of QI attributes, mu, beta, and the data distribution.

# global constants
k     = 100 # k-anonymity guarantee
delta = 1   # maximum time delay (in seconds)
beta  = 10  # maximum number of non-anonymised clusters
mu    = 100 # mu corresponds to the number of most recent ks-anonymised clusters on which tau is calculated
beta  = 50  # beta is the threshold for controlling the maximum number of non-ks-anonymized clusters in memory

# TODO how do we keep track of the mu **most recent** ks-anonymized clusters?
# - firstly we shouldnt keep the clusters in sets, but in a list

# the attribute headers is a global value that is defined when the stream starts
# for now the quasi-identifiers are defined to be all the attributes of the tuple
attribute_headers = None
quasi_identifiers = None

async def stream():
    """Opens a csv file and starts outputting its elements as a stream."""
    with open('datasets/credit_data.csv') as f:
        data = DataSet(f)
        attribute_headers = DataSet.Headers
        row = data.getNextTuple()
        while(row!=None):
            row = data.getNextTuple()
            yield row
            await asyncio.sleep(1)

        '''csv_reader = csv.reader(f)
        first_line = True
        for row in csv_reader:
            if first_line:
                attribute_headers = tuple(row)
                quasi_identifiers = attribute_headers
                first_line = False
                continue
            yield tuple(row)
            await asyncio.sleep(1)'''
    
def v_info_loss(attribute, u, l, U, L):
    """Computes a General Loss Metric adapted to streaming data."""
    if attribute.is_categorical():
        return (S_v - 1) / (S - 1)
    elif attribute.is_linear():
        return (u - l) / (U - L)


def info_loss(g:tuple):
    """g is a tuple generalization."""
    return sum([v_info_loss() for v in g]) * len(g)


# def Enlargement(C, t:tuple):

#     return sum([v_info_loss() - v_info_loss() for ]) / n

# def best_selection(t): 
#     E = set()
#     for C_j in gamma:
#         e = Enlargement(C_j, t)
#         E.add(e)
#     _min_ = min(E)
#     SetCMin = {c for c in gamma if Enlargement(c, t) == _min_}
#     for C_j in SetCMin:
#         pass
#     if len(SetCok) == 0:
#         if pass:
#             pass
#         else:
#             return None
#     else:
#         return a cluster in SetCMin with minimum size

def output_cluster(C: Cluster, tau: float, gamma: set[Cluster], omega: list[Cluster]):
    """Adds a cluster to the set of ks-anonymized clusters. But before that, attempts to split the cluster to minimize information loss."""
    global k
    if len(C) >= 2*k: # verify if C has the minimum size to be split
        sc = split(C)
    else:
        sc = [C]
    for c in sc:
        # output all tuples in ci with its generalization

        # tau is updated to be the average information loss of the mu most recent ks-anonymized clusters including the new ones
        tau = sum(info_loss(cl) for cl in omega[:-mu]) / mu
        if info_loss(c) < tau:
            # add the cluster to the set of k-anonymised clusters
            omega.add(c)
        gamma.remove(c)

def delay_constraint(t, gamma):
    global k
    # let C be the non-k_s anonymized cluster to which t belongs
    C = Cluster()
    if len(C) >= k:
        output_cluster(C) # what does that do
    else:
        kc_set = set() # the non-empty clusters in Omega containing t
        if len(kc_set) > 0:
            kc = random.choice(kc_set)
            return
        m = 0
        for c in gamma:
            if len(C) < len(c):
                m += 1
        if m > len(gamma) / 2:
            # suppress tuple t
            return
        if sum(len(c) for c in gamma) < k:
            suppress(t)
            return
        ouptput_cluster(merge_clusters(C, ))

def split(C) -> list[Cluster]:
    """Splits a cluster based on the KNN algorithm"""
    pass

async def castle(stream, k, delta, beta):
    gamma = set() # set of non k_s anonymized clusters
    omega = []    # list of k_s anonymized clusters
    tau = 0       # threshold on the information loss
    async for t in stream():
        C = best_selection(t)
        if C is None:
            gamma.add(Cluster(t))
        else:
            C.add(t)
        t_prime = t.p - delta # ??
        # if t_prime has not yet been output:
        #     delay_constraint(t_prime)

async def process():
    async for t in stream():
        print(t)


if __name__ == "__main__":
    asyncio.run(process())
    # asyncio.run(castle(
    #     stream = stream(),
    #     k = k,
    #     delta = delta,
    #     beta = beta
    # ))
