import csv
import asyncio

from cluster import Cluster
from Attribute import Attribute
from DataSet import DataSet
from DataSetFactory import DataSetFactory

# the attribute headers is a global value that is defined when the stream starts
# for now the quasi-identifiers are defined to be all the attributes of the tuple
# attribute_headers = None
# quasi_identifiers = None

async def stream():
    """Opens a csv file and starts outputting its elements as a stream."""
    with open('datasets/credit_data.csv') as f:
        data = DataSetFactory.createCreditData(f)
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
    
def v_info_loss():
    pass


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

def delay_constraint(t):
    pass

def ouptput_cluster(t):
    pass

def split(C):
    # initialise SC to be empty
    # let BS be the buckets created by grouping tuples in C by pid attribute
    # while |BS|>=k:
        # Randomly select a bucket Bbar from BS and pick one of its tuples tbar
        # create a bew sub-cluster Cnew over tbar
        # if Bbar is empty:
            # delete Bbar
        # let H_(k-1) be a heap with k-1 nodes, each with an infinite distance to tbar
        # foreach bucket in BS\Bbar do
            # pick one of its tuples t, and calculate t's distance to tbar
            # if t is closer to tbar than the root of H_(k-1):
                # t replaces the root, and H_(k-1) is adjusted accordingly
        # foreach node in H_(k-1):
            # let tbar be the tuple in the node
            # insert tbar into Cnew
            # Let B_j be the bucket containing tbar
            # delete tbar from B_j
            # if B_j is empty:
                # delete B_j
        # add Cnew to SC
    # foreach B_i in BS:
        # pick a tuple t_i in B_i
        # find t_i's nearest cluster in SC, and add all the tuples in B_i to it
        # delete B_i
    # return SC
    pass

async def castle(stream, k, delta, beta):
    gamma = set() # set of k_s anonymized clusters
    omega = set() # set of non k_s anonymized clusters
    tau = 0
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
    #     k = 1,
    #     delta = 1,
    #     beta = 1
    # ))
