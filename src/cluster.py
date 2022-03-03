from copy import deepcopy

import main
import random

class Cluster(object):
    
    """ A cluster object to store a collection of similar tuples """

    def __init__(self, headers):
        # list of all tuples in the cluster
        self.tuples = []
        # generalised range of attribute values
        self.ranges = {}
        for header in headers:
            self.ranges[header] = []
        # self.set_of_data = {}
        # for header in headers:
        #     self.set_of_data[header] = []
    
    def add_to_cluster(self, t):
        """ Adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(t)
        for attr_head, data in zip(main.attribute_headers, t):
            # update ranges of the attribute's values
            if len(self.ranges[attr_head]) == 0:
                self.ranges[attr_head] = [data]
            elif len(self.ranges[attr_head]) == 1:
                if data > self.ranges[attr_head][0]:
                    self.ranges[attr_head].append(data)
                elif data < self.ranges[attr_head][0]:
                    self.ranges[attr_head].insert(0, data)
            elif len(self.ranges[attr_head]) == 2:
                if data > self.ranges[attr_head][1]:
                    self.ranges[attr_head][1] = data
                elif data < self.ranges[attr_head][0]:
                    self.ranges[attr_head][0] = data
            # if not data in self.set_of_data[attr_head]:
            #     self.set_of_data[attr_head].append(data)

    def remove_from_cluster(self, t):
        """ Removes a tuple from the cluster """
        self.tuples.remove(t)

    def get_generic(self, t):
        """ Gets a generic form of tuple data from the selection in the cluster. 
            The output tuple has attributes for the range of possible values and a specific value taken from the set. """
        gen_tuple = {}
        for header, header_range in self.ranges.items():
            print(header)
            if header in main.quasi_identifiers:
                gen_tuple['min_' + header] = header_range[0]
                gen_tuple['max_' + header] = header_range[1]

        return gen_tuple
    
    def __len__(self):
        """Returns the quantity of tuples in the cluster"""
        return len(self.tuples)

    def count_distinct_tuples(self):
        """Returns the quantity of distinct tuples in the cluster"""
        set_tuples = set(self.tuples)
        return len(set_tuples)