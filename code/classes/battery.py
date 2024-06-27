
import classes
import functions

class Battery:
    def __init__(self, cords, capacity, id):
        """Battery Node on grid"""
        self.id = id
        self.cords = cords   
        self.max_capacity = -capacity
        self.reset()

    def viability(self, output):
        if output != None:
            if isinstance(output, classes.House):
                output = output.output
            if self.capacity + output <= 0:
                return True
        return False

    def update(self):
        data = functions.analyse_network(self)
        if data != False:
            self.apply_data(data)

    def apply_data(self, data):
        if data != False:
            self.capacity = self.max_capacity + data[0]
            self.cost = data[1]
            self.network = data[2]
            self.houses = data[3]

    def reset(self):
        self.capacity = self.max_capacity
        self.houses = set()
        self.cables = set()
        self.network = ()
        self.cost = 0

    def __eq__(self, other):
        if isinstance(other, Battery):
            return (self.cords) == (other.cords)
        return False

    def __hash__(self):
        return hash(self.cords)

    def __repr__(self):
        return f"Battery{self.cords}"