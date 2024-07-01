
import classes
import functions

class Battery:
    def __init__(self, cords, capacity, id):
        """Battery Node on grid"""
        self.id = id
        self.cords = cords   
        self.max_capacity = -capacity
        self.connections = set()

        # variables to store old state
        self.previous_connections = set()
        self.previous_cost = 0
        self.reset()

    def viability(self, house):
        if self.capacity + house.output <= 0:
            return True
        return False

    def reset(self):
        self.capacity = self.max_capacity
        self.houses = []
        self.cost = 0

    def __eq__(self, other):
        if other != None:
            return (self.cords) == (other.cords)
        return False
    
    def __lt__(self, other):
        # Custom less than method to allow Node comparison in priority queue
        return (self.cords) < (other.cords)
    
    def __hash__(self):
        return hash(self.cords)

    def __repr__(self):
        return f"Battery{self.cords}"