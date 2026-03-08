import sys 
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

import pytest
from network import Network
from graph import Graph

#Tests by cheking if the graph printed as a sting corresponds to the expected extended graph.
#Extended graph string generated and checked by AI beforehand

def test_extended_graph_small():
    network = Network.from_file(NET_DIR / "small.txt")
    graph = network.build_extended_graph()
    assert str(graph) == "{('lozere', 0): [(('ensae', 2), 10), (('guichet', 0), 20)], ('lozere', 1): [(('ensae', 3), 20), (('guichet', 1), 40)], ('lozere', 2): [(('ensae', 4), 30), (('guichet', 2), 60)], ('lozere', 3): [(('ensae', 5), 40), (('guichet', 3), 80)], ('lozere', 4): [(('ensae', 6), 50), (('guichet', 4), 100)], ('lozere', 5): [(('guichet', 5), 120)], ('lozere', 6): [(('guichet', 6), 140)], ('ensae', 0): [(('saclay', 0), 45)], ('ensae', 1): [(('saclay', 1), 90)], ('ensae', 2): [(('saclay', 2), 135)], ('ensae', 3): [(('saclay', 3), 180)], ('ensae', 4): [(('saclay', 4), 225)], ('ensae', 5): [(('saclay', 5), 270)], ('ensae', 6): [(('saclay', 6), 315)], ('guichet', 0): [(('ensae', 1), 15)], ('guichet', 1): [(('ensae', 2), 30)], ('guichet', 2): [(('ensae', 3), 45)], ('guichet', 3): [(('ensae', 4), 60)], ('guichet', 4): [(('ensae', 5), 75)], ('guichet', 5): [(('ensae', 6), 90)], ('guichet', 6): [], ('saclay', 0): [], ('saclay', 1): [], ('saclay', 2): [], ('saclay', 3): [], ('saclay', 4): [], ('saclay', 5): [], ('saclay', 6): []}"