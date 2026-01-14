import functions
import classes 

def scan_path(node, other_node, composition = [0, 0], scanned_cables = None):
    if scanned_cables == None:
        scanned_cables = set()
    found_battery = False
    if node == other_node:
        composition = [0, 1]
    if isinstance(node, classes.Battery):
        if composition == [0, 0]:
            composition = [1, 0]
        return composition, True
    for cable in node.cables:
        if found_battery == False and cable not in scanned_cables:
            scanned_cables.add(cable)
            composition, found_battery = scan_path(cable.other(node), other_node, composition, scanned_cables)
    if node == other_node and found_battery == False:
        return [0, 0], False
    return composition, found_battery

def get_structure(cableA, cableB):
    cables = [cableA, cableB]
    composition = [[], []]
    for i in range(0, 2):
        if isinstance(cables[i].node1, classes.Cable):
            composition[i] = [1, 0]
        elif isinstance(cables[i].node2, classes.Cable):
            composition[i] = [0, 1]
        else: 
            composition[i] = scan_path(cables[i].node1, cables[i].node2)[0]
    
    if cableA.node1 in [cableB.node1, cableB.node2] or cableA.node2 in [cableB.node1, cableB.node2]:
        return composition, 3
    return composition, 4

def n_nodes(cableA, cableB):
    if cableA.node1 in [cableB.node1, cableB.node2] or cableA.node2 in [cableB.node1, cableB.node2]:
        return 3
    return 4
    

    


