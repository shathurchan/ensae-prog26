from heapq import *
"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""


class Graph:
    """
    A minimal class for directed weighted graph represented as adjacency list. 
    
    Attributes: 
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight.
        Ex: edges = {v0: [(v1, 21), (v2, 12)], 
                     v1: [(v0, 74), (v2, 32)], 
                     ...}

    Methods: 
    --------
    neighbours(self, node): 
        Returns the list of all neighbors of a node
    
    graph_shortest_path(self, point1, point2): 
        Uses Dijkstra's algorithm to find the optimal path between two nodes (points) on the graph : point1 and point2
    """

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]
    
    def __str__(self): 
        """
        Prints the graph as text.
        """
        output = f"A graph with {len(self._edges)} nodes and the following adjacency list:\n"
        return output+self._edges.__str__()
    

    def graph_shortest_path(self, point1, point2):
        #Dijkstra algorithm used to solve the sortest path problem
        #Problem : Dijsktra only returns cost and list of parent nodes that were tested, path needs to be reconstructed latre
        #Used the same type of heap as in Simon Mauras' Robot heap solve
        q = [(0, point1)]
        dist = {point1: 0}
        parent = {}
        visited = set()
        while q:
            cost, current_point = heappop(q)
            if current_point in visited:
                continue
            visited.add(current_point)
            if current_point == point2:
                break
            for v, w in self.neighbours(current_point):
                new_cost = cost + w
                if new_cost < dist.get(v, float("inf")):
                    dist[v] = new_cost
                    parent[v] = current_point
                    heappush(q, (new_cost, v))

        if point2 not in dist:
            return float("inf"), []
        #Reconstruct path using nodes tested
        path = []
        node = point2
        while node != point1:
            path.append(node)
            node = parent[node]
        path.append(point1)
        path.reverse()
        return dist[point2], path


class GraphImplicit(Graph):
    """
    A class representing a network as an underlying graph, with both distance and fatigue coefficients
    
    Attributes: 
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight and fatigue.
        Ex: edges = {v0: [(v1, 21), (v2, 12)], 
                     v1: [(v0, 74), (v2, 32)], 
                     ...}

    Methods: 
    --------
    neighbours(self, node): 
        Returns the list of all neighbors of a node accouting for the fatigue coefficient via the given formula
    
    """
     
    def __init__(self, network):
        self.network = network
    
    def __str__(self):
        """
        Prints the implicit graph as text.
        """
        output = f"A graph with {len(self.network._roads)} nodes and the following adjacency list:\n"
        return output+self.network._roads.__str__()
  
    def neighbours(self, state):
        v, f = state
        routes = self.network._roads.get(v, [])
        result = []
        for voisin, longueur, fatigue_arete in routes:
            new_fatigue = f + fatigue_arete
            cost = longueur * (1 + f)   
            result.append(((voisin, new_fatigue), cost)) 
        return result
