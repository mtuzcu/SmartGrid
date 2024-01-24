# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

from ..universal import *

def random_algorithm(Grid: object, component: object):
    """random algorithm"""

    # TODO
    # select random house to connect to
    random_component = random.get_random_component(component)
    
    # add that house to end connection of batery and house
    Grid.connect_components(random_component, component)
