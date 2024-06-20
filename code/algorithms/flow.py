# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
import functions

def flow_algorithm(grid):
    create_super_nodes(grid)
    set_edges(grid)
    check_edges(grid)
    for edge in grid.sink.edges:
        print(edge.other_node(grid.sink).capacity)

    total_output = grid.source.capacity
    total_flow = 0

    while total_flow < total_output * 0.9:
        
        shortest_path(grid)
        if grid.sink.distance == float('inf'):
            break
        path_flow = augment_flow(grid)
        total_flow += path_flow
        grid.total_cost_cables += path_flow * grid.sink.distance
    
    print('cost: ',{grid.total_cost_cables})
    print(total_flow)
    print_connections(grid)

def create_super_nodes(grid):
        """set the requirements up to use the flow algorithm"""
        grid.source = Node(grid, (-1, 0))
        grid.source.id = 3
        for house in grid.houses:
            grid.connect(grid.source, house, 0)
            grid.source.capacity += house.capacity
        
        grid.sink = Node(grid, (0, -1))
        grid.sink.id = 3
        for battery in grid.batteries:
            grid.connect(battery, grid.sink, 0)
            grid.sink.capacity += battery.capacity

def set_edges(grid):
    for house in grid.houses:
        for battery in grid.batteries:
            grid.connect(house, battery)

def check_edges(grid):
    for node in grid.houses:
        if node.capacity > 0:  # This is a house node
            if len(node.edges) != len(grid.batteries) + 1:
                print(f"House at ({node.cords}) incorrect amount of edges")
    for node in grid.batteries:
        if node.capacity > 0:  # This is a house node
            if len(node.edges) != len(grid.houses) + 1:
                print(f"Battery at ({node.cords}) incorrect amount of edges")

# shortest path
def shortest_path(grid):
    reset_distance(grid)
    in_queue = {node: False for row in grid.nodes for node in row}
    source = grid.source 
    source.distance = 0
    queue = [(0, source)]
    in_queue[source] = False
    in_queue[grid.sink] = False
    
    while queue:
        d, u = heapq.heappop(queue)
        if in_queue[u] == True or u.id == 0:
            continue
        in_queue[u] = True
        
        for edge in u.edges:
            v = edge.other_node(u)
    
            if edge.capacity > edge.flow and v.distance > u.distance + edge.cost:
                v.distance = u.distance + edge.cost
                v.parent = u
                heapq.heappush(queue, (v.distance, v))

def reset_distance(grid):
    grid.source.distance = 0
    grid.sink.distance = float('inf')
    for row in grid.nodes:
        for node in row:
            node.distance = float('inf')  
                   
    
def augment_flow(grid):
    source = grid.source
    sink = grid.sink
    
    # Find the bottleneck capacity along the path
    path_flow = float('inf')
    v = sink
    while v != source:
        u = v.parent

        # Find the cable connecting u and v
        for edge in u.edges:
            if edge.node1 == v or edge.node2 == v:
                path_flow = min(path_flow, edge.capacity - edge.flow)
                break
        v = u
    
    # Augment the flow along the path
    v = sink
    while v != source:
        u = v.parent

        # Find the cable connecting u and v
        for edge in u.edges:
            if edge.node1 == v or edge.node2 == v:
                edge.flow += path_flow

                # Update the reverse flow
                if edge.node1 == u:
                    edge.capacity += -path_flow
                else:
                    edge.capacity += path_flow
                break
        v = u
    
    return path_flow

def print_connections(grid):
    connections = set()
    for row in grid.nodes:
        for node in row:
            if node.id != 0:
                for edge in node.edges:
                    if edge.flow > 0 and edge.node1 != grid.source and edge.node2 != grid.sink:
                        house = edge.node1 if edge.node1.capacity > 0 else edge.node2
                        battery = edge.other_node(house)
                        connection = ((house.cords), (battery.cords))
                        if connection not in connections:
                            grid.connect(house, battery, 1)
                            connections.add(connection)
                        #print(f"House at ({house.cords}) is connected to Battery at ({battery.cords}) with flow {edge.flow}")

# Example call to the function after running the flow algorithm




            