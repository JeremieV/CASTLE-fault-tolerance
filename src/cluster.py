from __future__ import annotations
from copy import deepcopy
from pickle import TRUE

# import main
import random
from xml.dom.minidom import Attr
from DataSet import DataSet
from Attribute import Attribute
from typing import Tuple, List

from tupleWrapper import TupleWrapper

class Cluster(object):
    
    """ A cluster object to store a collection of similar tuples """

    def __init__(self, ds: DataSet):
        # list of all tuples in the cluster
        self.tuples:List[TupleWrapper] = []
        # generalised range of attribute values
        self.ranges = {}
        # for attr in ds.getQuasiIdentifiers():
        for attr in ds.getAttributes():
            self.ranges[attr] = []
        self.ds: DataSet = ds
    
    def add_to_cluster(self, t: TupleWrapper):
        """ Adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(t)
        attribute: Attribute
        for attribute, data in zip(self.ds.getAttributes(), t.Content):
            if (attribute.isQI()):
                self.ranges[attribute] = attribute.expandRange(self.ranges[attribute], data)

    def enlarge(self, other_cluster: Cluster):
        for t in other_cluster.tuples:
            self.add_to_cluster(t)

    def remove_from_cluster(self, t):
        """ Removes a tuple from the cluster """
        self.tuples.remove(t)
    
    def contains(self, t):
        return t in self.tuples

    def output_cluster(self):
        """ Outputs a tuple of strings representing an anonymised form of the cluster of tuples where quasi-identifiers 
            are replaced with ranges of values that appear in the cluster for that attribute"""
        output: list(tuple) = list()
        for t in self.tuples:
            output.append(self.get_generic(t))
        return tuple(output)
    
    def get_buckets(self) -> List[List[Tuple]]:
        """group tuples into 'buckets' that share the same pid value"""
        buck_dict: dict(list()) = {}
        buckets: list(list(tuple)) = list(list())
        for tuple in self.tuples:
            for attr, data in zip(self.ds.getAttributes(), tuple):
                if attr.isPID():
                    buck_list: list() = buck_dict.get(data)
                    buck_list.append(tuple)
                    break
        for bucket in buck_dict.values():
            buckets.append(bucket)
        return buckets


    def get_generic(self, tuple):
        """ Gets a generic form of a tuple where quasi-identifiers are replaced with ranges of values 
            that appear in the cluster for that attribute """
        output_string = ""
        attr: Attribute
        for attr in self.ds.getAttributes():
            if attr.isQI():
                output_string = output_string + attr.getName() + attr.getGeneralization(self.ranges[attr]) + " "
            else:
                non_quasi_value = attr.getValue(tuple)
                non_quasi_range = [non_quasi_value, non_quasi_value]
                output_string = output_string + attr.getName() + attr.getGeneralization(non_quasi_range) + " "
        return output_string
    
    #return the information loss of a cluster
    #if a tuple is supplied, then return the info loss of the enlarged cluster
    def get_info_loss(self, tuple:TupleWrapper=None):
        sum_info_loss = 0
        n = 0
        for clus_tuple in self.tuples:
            attribute: Attribute
            if tuple is None:
                for attribute in self.ds.getAttributes():
                    # if not a QI, the range will be 0 so the info loss will be 0
                    if attribute.isQI():
                        sum_info_loss += attribute.calculateInfoLoss(self.ranges[attribute])
                        n += 1
            else:
                for attribute, data in zip(self.ds.getAttributes(), tuple.Content):
                    # if not a QI, the range will be 0 so the info loss will be 0
                    if attribute.isQI():
                        new_range = attribute.expandRange(self.ranges[attribute], data)
                        sum_info_loss += attribute.calculateInfoLoss(new_range)
                        n += 1
        return sum_info_loss/n
    
    def __len__(self):
        """Returns the quantity of tuples in the cluster"""
        return len(self.tuples)
    
    def size(self):
        return len(self)

    def count_distinct_tuples(self):
        """Returns the quantity of distinct tuples in the cluster"""
        set_tuples = set(self.tuples)
        return len(set_tuples)