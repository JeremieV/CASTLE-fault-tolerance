import csv
import asyncio

from cluster import Cluster

# def main():
#     print("main is running")
#     cluster1 = cluster.Cluster()
    
#     # demo data
#     demoTuple = ("Tim", 21, "Computer Science", "M")
#     cluster1.add_to_cluster(demoTuple)
#     print("ranges: " + str(cluster1.ranges))
#     demoTuple = ("Callum", 20, "Computer Science", "M")
#     cluster1.add_to_cluster(demoTuple)
#     print("ranges: " + str(cluster1.ranges))
#     demoTuple = ("Xindi", 21, "Data Science", "F")
#     cluster1.add_to_cluster(demoTuple)
#     print("ranges: " + str(cluster1.ranges))
#     demoTuple = ("Jeremie", 22, "Discrete Maths", "M")
#     cluster1.add_to_cluster(demoTuple)
#     print("ranges: " + str(cluster1.ranges))

#     print(cluster1.tuples)
#     cluster_size = cluster1.__len__()
#     print("cluster size: " + str(cluster_size))
    

# if __name__ == "__main__":
#     main()

async def stream():
    with open('datasets/credit_data.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            yield tuple(row)
            await asyncio.sleep(1)
    
def Enlargement():
    pass

def best_selection(t): 
    E = set()
    for C_j in gamma:
        e = Enlargement(C_j, t)
        E.add(e)
    _min_ = min(E)
    SetCMin = {c for c in gamma if Enlargement(c, t) == _min_}
    for C_j in SetCMin:
        pass
    if len(SetCok) == 0:
        if pass:
            pass
        else:
            return None
    else:
        return a cluster in SetCMin with minimum size

def delay_constraint(t):
    pass

def ouptput_cluster(t):
    pass

def split(C):
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