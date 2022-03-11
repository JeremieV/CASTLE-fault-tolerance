from copy import deepcopy
from pickle import TRUE

# import main
import random
from xml.dom.minidom import Attr
from DataSet import DataSet
from Attribute import Attribute

class Cluster(object):
    
    """ A cluster object to store a collection of similar tuples """

    def __init__(self, ds: DataSet):
        # list of all tuples in the cluster
        self.tuples = []
        # generalised range of attribute values
        self.ranges = {}
        for attr in ds.getQuasiIdentifiers():
            self.ranges[attr] = []
        self.ds = ds
    
    def add_to_cluster(self, t):
        """ Adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(t)
        for attribute, data in zip(self.ds.getAttributes(), t):
            if (attribute.isQI()):
                self.ranges[attribute] = attribute.expandRange(self.ranges[attribute], data)
            # update ranges of the attribute's values
            # if len(self.ranges[attr_head]) == 0:
            #     self.ranges[attr_head] = [data]
            # elif len(self.ranges[attr_head]) == 1:
            #     if data > self.ranges[attr_head][0]:
            #         self.ranges[attr_head].append(data)
            #     elif data < self.ranges[attr_head][0]:
            #         self.ranges[attr_head].insert(0, data)
            # elif len(self.ranges[attr_head]) == 2:
            #     if data > self.ranges[attr_head][1]:
            #         self.ranges[attr_head][1] = data
            #     elif data < self.ranges[attr_head][0]:
            #         self.ranges[attr_head][0] = data
            # if not data in self.set_of_data[attr_head]:
            #     self.set_of_data[attr_head].append(data)

    def remove_from_cluster(self, t):
        """ Removes a tuple from the cluster """
        self.tuples.remove(t)

    def get_generic(self):
        """ Gets a generic form of tuple data from the selection in the cluster. 
            The output tuple has attributes for the range of possible values and a specific value taken from the set. """
        gen_tuple = {}
        for attr, attr_range in self.ranges.items():
            # gen_tuple['min_' + attr.getName()] = attr_range[0]
            # gen_tuple['max_' + attr.getName()] = attr_range[1]
            gen_tuple[attr.getName()] = attr.getGeneralization((gen_tuple[attr.getName()][0], gen_tuple[attr.getName()][1]))
        return gen_tuple
    
    def __len__(self):
        """Returns the quantity of tuples in the cluster"""
        return len(self.tuples)

    def count_distinct_tuples(self):
        """Returns the quantity of distinct tuples in the cluster"""
        set_tuples = set(self.tuples)
        return len(set_tuples)