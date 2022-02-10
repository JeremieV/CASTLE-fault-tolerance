class Cluster(object):
    
    """ A cluster object to store a collection of similar tuples """

    def __init__(self):
        # list of all tuples in the cluster
        self.tuples = []
        # generalised range of attribute values
        self.ranges = [[]]
        print("cluster created")
    
    def add_to_cluster(self, tuple):
        """ adds the tuple to the cluster and performs range enlargement if needed """
        self.tuples.append(tuple)
        position = 0
        for attribute in tuple:
            # adds additional attribute range if it doesn't already exist
            if len(self.ranges) < position+1:
                self.ranges.append([attribute])
            if len(self.ranges[position]) == 0:
                self.ranges[position] = [attribute]
            elif len(self.ranges[position]) == 1:
                if attribute > self.ranges[position][0]:
                    self.ranges[position].append(attribute)
                elif attribute < self.ranges[position][0]:
                    self.ranges[position].insert(0, attribute)
            elif len(self.ranges[position]) == 2:
                if attribute > self.ranges[position][1]:
                    self.ranges[position][1] = attribute
                elif attribute < self.ranges[position][0]:
                    self.ranges[position][0] = attribute
            position+=1
    
    def __len__(self):
        return len(self.tuples)