import functions
import heapq

def prim_mst(network):
    """
    Prim's algorithm to find the Minimum Spanning Tree (MST) of a graph with dynamically generated edges.

    Parameters:
    nodes (list): List of nodes in the graph. Each node is represented as a tuple (name, (x, y)).

    Returns:
    list: Edges in the MST.
    """
    mst = []
    visited = set()
    priority_queue = []

    def add_edges(node):
        visited.add(node)
        for other_node in network:
            if other_node not in visited:
                weight = functions.manhattan_distance(node, other_node)
                heapq.heappush(priority_queue, (weight, node, other_node))

    # Start from the first node (assumed to be the battery)
    add_edges(network[0])

    while priority_queue:
        weight, node1, node2 = heapq.heappop(priority_queue)
        for node in network:
            if node[0] == node2 and node not in visited:
                mst.append((node1, node2, weight))
                add_edges(node)
                break
    print(mst)
    return mst