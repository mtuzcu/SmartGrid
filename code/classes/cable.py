# cable Object
import functions

class Cable:
    _counter = 0  # Class attribute to keep track of instances
    def __init__(self, node1, node2):
        """Node on grid containing node data"""
        self.node1 = node1
        self.node2 = node2
        self.cost = functions.manhatten_distance(node1, node2)
    
    def other(self, node):
        if node == self.node1:
            return self.node2
        if node == self.node2:
            return self.node1
        return None

    def __eq__(self, other):
        if isinstance(other, Cable):
            return ((self.node1 == other.node21 or self.node1 == other.node2) and (self.node2 == other.node1 or self.node2 == other.node2))
        return False
    
    def __hash__(self):
        return hash(frozenset([self.node1, self.node2]))
    
    def __repr__(self):
        return f"Cable({self.node1}, {self.node2})"
    



    #def __hash__(self):
    #    return hash(frozenset([self.cords1, self.cords2]))
    # def __eq__(self, other):
       # if self.cords1 in [other.cords1, other.cords2] and self.cords2 in [other.cords1, other.cords2]:
        #    return True