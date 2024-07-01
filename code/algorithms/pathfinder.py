import functions
import heapq
from collections import defaultdict

def prim_algorithm(battery):
    """uses prim algo"""
    processed_nodes = set()
    priority_queue = []
    minimum_spanning_tree = []
    network = [battery] + battery.houses

    def add_edges(node):
        processed_nodes.add(node)
        for other_node in network:
            if other_node not in processed_nodes:
                distance = functions.manhattan_distance(node, other_node)
                heapq.heappush(priority_queue, (distance, node, other_node))

    # Start algorithm from battery node
    add_edges(battery)

    while priority_queue:
        distance, node1, node2 = heapq.heappop(priority_queue)
        if node2 not in processed_nodes:
            minimum_spanning_tree.append((node1, node2, distance))
            add_edges(node2)

    return minimum_spanning_tree

def optimal_paths(minimum_spanning_tree):
    """gets mst"""
    cable_paths = []
    grid_utilization = defaultdict(int)
    total_cost = 0

    for edge in minimum_spanning_tree:
        x1, y1 = edge[0].cords
        x2, y2 = edge[1].cords

        # Calculate two possible paths. path1 is horizontal-vertical and path2 is vertical-horizontal
        path1 = [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)] + [(x2, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
        path2 = [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)] + [(x, y2) for x in range(min(x1, x2), max(x1, x2) + 1)]

        # Calculate cost of each possible path
        path1_cost = sum(grid_utilization[point] for point in path1)
        path2_cost = sum(grid_utilization[point] for point in path2)

        # Choose optimal path
        chosen_path = path1 if path1_cost <= path2_cost else path2
        chosen_cost = path1_cost if path1_cost <= path2_cost else path2_cost

        # Update grid utilization
        for cord in chosen_path:
            grid_utilization[cord] += 1
        
        # store the 2 or 3 necessary key points to draw the connection
        if chosen_path == path1:
            mid_point = (x2, y1) if x1 != x2 and y1 != y2 else None
        else:
            mid_point = (x1, y2) if x1 != x2 and y1 != y2 else None
        cable_paths.append((edge[0].cords, mid_point, edge[1].cords))

        # Add the cost of this path to the total cost
        total_cost += len(chosen_path) - chosen_cost

    return cable_paths, total_cost

def optimal_network(battery):
    minimum_spanning_tree = prim_algorithm(battery)
    battery.connections, battery.cost = optimal_paths(minimum_spanning_tree)
    return 

