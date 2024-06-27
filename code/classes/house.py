# house object
import classes
import classes.battery
import functions

class House:
    def __init__(self, cords, output):
        """Node on grid containing node data"""
        self.cords = cords   
        self.output = output

        # stored connected houses and own cables
        self.cables = set()

    def reset(self):
        self.cables = set()

    def __eq__(self, other):
        if isinstance(other, House):
            return (self.cords) == (other.cords)
        return False
    
    def __hash__(self):
        return hash(self.cords)

    def __repr__(self):
        return f"House{self.cords}"