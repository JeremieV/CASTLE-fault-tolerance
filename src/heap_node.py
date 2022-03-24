import sys


class HeapNode:
    
    def __init__(self, t=None, distance=None):
        if t is not None:
            self.tuple: tuple = t
        else:
            self.tuple: tuple
        if distance is not None:
            self.distance: int = distance
        else:
            self.distance: int = sys.maxsize
    
    def set_tuple(self, t, distance):
        self.tuple = t
        self.distance = distance
    
    def get_tuple(self):
        return self.tuple
    
    def get_distance(self):
        return self.distance