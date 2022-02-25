from copy import deepcopy
from tuple_obj import TupleObj

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
        self.set_of_data = {}
        for header in headers:
            self.set_of_data[header] = []
    
    def add_to_cluster(self, t: TupleObj):
        """ Adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(t)
        for attr_head, data in zip(t.attribute_headers, t.data):
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
            if not data in self.set_of_data[attr_head]:
                self.set_of_data[attr_head] = data

    def remove_from_cluster(self, t: TupleObj):
        """ Removes a tuple from the cluster """
        self.tuples.remove(t)

        # todo update the set_of_data to remove values if they are no longer in the cluster
        

    def get_generic(self, t: TupleObj):
        """ Gets a generic form of tuple data from the selection in the cluster. 
            The output tuple has attributes for the range of possible values and a specific value taken from the set. """
        gen_tuple = deepcopy(t)
        print(gen_tuple.qi_attributes)
        for header, header_range in self.ranges.items():
            print(header)
            if header in gen_tuple.qi_attributes:
                # pick a random value for each heading from tuples in the store
                gen_tuple.data.append(header_range[0])
                random_tuple = random.choice(self.tuples)
                for val, sample_header in zip(random_tuple.data, random_tuple.attribute_headers):
                    print(sample_header)
                    if header == sample_header:
                        gen_tuple.data.append(val)
                        print("appended val")
                        break
                gen_tuple.data.append(header_range[1])

                # add headers to the gen_tuple for the range of values
                gen_tuple.attribute_headers.append('min_' + header)
                gen_tuple.attribute_headers.append('gen_' + header)
                gen_tuple.attribute_headers.append('max_' + header)

            gen_tuple.data.pop(gen_tuple.attribute_headers.index(header))
            gen_tuple.attribute_headers.remove(header)

        return gen_tuple
    
    def __len__(self):
        return len(self.tuples)