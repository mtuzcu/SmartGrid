# house object
import classes
import classes.battery
import functions

class House:
    def __init__(self, cords, output):
        """Node on grid containing node data"""
        self.cords = cords   
        self.output = output
        self.battery = None

        # stored connected houses and own cables
        self.cables = set()

    def reset(self):
        self.battery = None

    def __eq__(self, other):
        if isinstance(other, House):
            return (self.cords) == (other.cords)
        return False
    
    def __lt__(self, other):
            # Custom less than method to allow Node comparison in priority queue
            return (self.cords) < (other.cords)
    
    def __hash__(self):
        return hash(self.cords)

    def __repr__(self):
        return f"House{self.cords}"