from graph import *

class Network:
    """
    Class for a network that represents the environment (with length and fatigue on roads). 
    """

    def __init__(self, roads={}, start=None, end=None):
        """
        Initializes the network from a dictionary roads. 

        Parameters: 
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list, that is 
            roads[u] = list of (v, length, fatigue)
            Ex: roads = {v0: [(v1, 21, 2), (v2, 12, 4)], 
                        v1: [(v0, 74, 2), (v2, 32, 1)], 
                        ...}
        start, end: 
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

    def __str__(self): 
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Network from an environment file.

        File format: one edge per line (start end length fatigue).
        """
        # Initialize adjacency list
        roads = {}

        with open(filename, "r") as testcase:
            nb, start, end = testcase.readline().strip().split()
            for _ in range(int(nb)):
                i, j, l, f = testcase.readline().strip().split()
                l, f = int(l), int(f)
                roads.setdefault(i, []).append((j, l, f))
                roads.setdefault(j, [])

        return cls(roads=roads, start=start, end=end)

    def build_simple_graph(self):
        """
        Builds an object of type Graph from the network, by ignoring the fatigue coefficient. 
        """
        # P1.Q1 Selects the keys of the _roads dictionary, adds the nodes to the graph by removing the fatigue
        edges = {}
        for keys, values in self._roads.items():
            edges[keys] = [(v, d) for (v, d, fatigue) in values]
        return Graph(edges)


    def build_extended_graph(self):
        """
        Builds an extended graph using the network, by implementing the fatigue coefficients as additional vertices in three dimensions.
        """
        # P1.Q2 Generates a graph with way more nodes adapting to multiple fatigue coefficients. The maximum fatigue to go up to is
        # F_max, it is determined using the data present in the network class. The function generates multiple copies of the same graph with fatigue coefficients up
        # to F_max copies. The graph_shortest_path function will operate on tuples to reach the best path given some initial and termnial
        # fatigue.
        max_fatigue = 0
        for v in self._roads:
            for (_, _, fatigue) in self._roads[v]:
                max_fatigue = max(max_fatigue, fatigue)

        #F_max is the maximum fatigue that can possibly be reached while going through the graph
        F_max = (len(self._roads) - 1) * max_fatigue
        print(F_max)

        extended_edges = {}
        for v in self._roads:
            for F in range(F_max + 1):
                extended_edges[(v, F)] = []

        for v in self._roads:
            for (w, length, fatigue) in self._roads[v]:
                for F in range(F_max + 1):
                    new_F = F + fatigue
                    if new_F <= F_max:
                        cost = length * (1 + F)
                        extended_edges[(v, F)].append(((w, new_F), cost))

        return Graph(extended_edges)
    
    def build_implicit_graph(self):
        return GraphImplicit(self)