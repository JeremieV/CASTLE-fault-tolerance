import csv
import asyncio
import random

from cluster import Cluster
from Attribute import Attribute
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

if __name__ == "__main__":
    # asyncio.run(process())
    # asyncio.run(castle(
    #     stream = stream(),
    #     k = k,
    #     delta = delta,
    #     beta = beta
    # ))
