import sys 
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

import pytest
from network import Network
from graph import Graph

#Tests by cheking if the shortest path in a small extended graph is valid
#Desired fatigue coefficients taken arbitrarily

def test_small_implicit_shortest_path():
    network = Network.from_file(NET_DIR / "small.txt")
    graph = network.build_implicit_graph()
    assert str(graph.graph_shortest_path(("lozere", 0), ("saclay", 2))) == "(145, [('lozere', 0), ('ensae', 2), ('saclay', 2)])"