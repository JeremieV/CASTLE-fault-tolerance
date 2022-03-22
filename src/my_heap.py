from logging import root

from heap_node import HeapNode


class MyHeap:

    def __init__(self, k):
        self.my_heap: list(HeapNode) = list()
        for i in range(k-2):
            node = HeapNode()
            self.my_heap.append(node)
    
    def add_to_heap(self, new_node: HeapNode):
        root_node: HeapNode = self.my_heap[0]
        if new_node.get_distance < root_node.get_distance:
            self.my_heap.pop()
            self.my_heap.insert(0, new_node)

    

    
