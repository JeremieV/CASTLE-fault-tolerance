import csv
import asyncio
import random
from CASTLE import CASTLE

from DataSet import DataSet
from DataSetFactory import DataSetFactory

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
# attribute_headers = None
# quasi_identifiers = None

async def stream(data):
    """Opens a csv file and starts outputting its elements as a stream."""
    row = data.getNextTuple()
    while(row!=None):
        row = data.getNextTuple()
        print("read")
        yield row
        await asyncio.sleep(1)

async def main():
    with open('datasets/credit_data.csv') as f:
        data = DataSetFactory.createCreditData(f)
        algorithm = CASTLE(data)
        async for i in stream(data):
            result = algorithm.readTuple(i)
            for r in result:
                print(r)

if __name__ == "__main__":
     asyncio.run(main())
