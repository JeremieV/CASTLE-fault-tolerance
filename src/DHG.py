from DHGTreeNode import DHGTreeNode
 
class DHG:

    def __init__(self, values):
        self.n_count = 1
        self.values = values
        self.root = DHGTreeNode('No generalisation', values, None)

    def addValue(self, value):
        self.values.append(value)

    # Generalise a single value to the 'gen_name' parameter
    def addGeneralisation(self, gen_name, gen_value):
        
        # Sanitisation to make sure value is in the tree
        if not (gen_value in self.root.values):
            return False

        # Add leaf to root if no generalisations exist
        if self.n_count == 1:
            self.root.addLeaf(gen_name, gen_value)
        else :

            # Search descends through the tree looking for the final node that the value exists in
            # Guaranteed to terminate, so uses a 'while True' loop
            # Multiples of the same generalisation nodes can exist in different places of the tree. This means that
            # currently the last generalisation you give for a node will be considered it's highest generalisation.
            # I can rework this if we want to ensure that there is uniform generalisation nodes, however as long as we
            # input the generalisations in a consistent order this shouldnt matter. (I've made an example showing this,
            # I'll put it in a testing folder)
            search_node = self.root
            while True:
                
                last_node = True
                for child in search_node.pointers:
                    
                    # Generalisation already exists in child node, so add to that node's values
                    if child.name == gen_name:
                        if not (gen_value in child.values):
                            child.values.append(gen_value)
                            return True
                        else:
                            return False
                    else:        
                        if gen_value in child.values:
                            if len(child.pointers) == 0:
                                child.addLeaf(gen_name, gen_value, child)
                                self.n_count += 1
                                return True
                            else: 
                                search_node = child
                                last_node = False
                                break
                    
                # Value does not exist in any children, so this node must be it's highest generalisation
                if last_node:
                    self.n_count += 1
                    search_node.addLeaf(gen_name, gen_value, search_node)
                    return True
            
    # Add multiple values from an array, values will be added to the tree sequentially, however the structure
    # of the tree should remain the same no matter the order
    def addMultipleGeneralisations(self, gen_name, values):

        for value in values:
            self.addGeneralisation(gen_name, value)
        return True
            
    def getHighestGeneralisation(self, search_value):

        search_node = self.root
        while len(search_node.pointers) > 0:
            
            value_found = False
            for child in search_node.pointers:
                
                if search_value in child.values:
                    search_node = child
                    value_found = True

            if not value_found:
                return search_node.name

        return search_node.name