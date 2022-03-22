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
        # for attr in ds.getQuasiIdentifiers():
        for attr in ds.getAttributes():
            self.ranges[attr] = []
        self.ds: DataSet = ds
    
    def add_to_cluster(self, t):
        """ Adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(t)
        attribute: Attribute
        for attribute, data in zip(self.ds.getAttributes(), t):
            if (attribute.isQI()):
                self.ranges[attribute] = attribute.expandRange(self.ranges[attribute], data)

    def remove_from_cluster(self, t):
        """ Removes a tuple from the cluster """
        self.tuples.remove(t)

    def output_cluster(self):
        """ Outputs a string representing an anonymised form of the cluster of tuples where quasi-identifiers 
            are replaced with ranges of values that appear in the cluster for that attribute"""
        output_string = ""
        for tuple in self.tuples:
            output_string = output_string + self.get_generic(tuple) + "\n"

        return output_string
    
    def get_buckets(self) -> list(list(tuple)):
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
            if attr.isQI:
                output_string = output_string + attr.getName() + attr.getGeneralization(self.attrRange) + " "
            else:
                non_quasi_value = attr.getValue(tuple)
                non_quasi_range = [non_quasi_value, non_quasi_value]
                output_string = output_string + attr.getName() + attr.getGeneralization(non_quasi_range) + " "
        return output_string
    
    def __len__(self):
        """Returns the quantity of tuples in the cluster"""
        return len(self.tuples)

    def count_distinct_tuples(self):
        """Returns the quantity of distinct tuples in the cluster"""
        set_tuples = set(self.tuples)
        return len(set_tuples)