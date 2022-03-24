import sys


class HeapNode:
    
    def __init__(self, t=None, distance=None):
        if t is not None:
            self.tuple: tuple = t
        
        if distance is not None:
            self.distance: int = distance
    
    def set_tuple(self, t, distance):
        self.tuple = t
        self.distance = distance
    
    def get_tuple(self):
        return self.tuple
    
    def get_distance(self):
        return self.distance