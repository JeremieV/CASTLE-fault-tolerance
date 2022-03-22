import sys


class HeapNode:
    
    def __init__(self):
        self.tuple: tuple
        self.distance = sys.maxint
    
    def __init__(self, t, distance):
        self.tuple: tuple = t
        self.distance: int = distance
    
    def set_tuple(self, t, distance):
        self.tuple = t
        self.distance = distance
    
    def get_tuple(self):
        return self.tuple
    
    def get_distance(self):
        return self.distance