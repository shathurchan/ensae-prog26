import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

from network import Network


def test_chemin_graphe_simple():
    """
    Graphe sans fatigue (question 1) sur small.txt.
    Chemin optimal : lozere -> ensae -> saclay
    Distance : 10 + 45 = 55
    """
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_simple_graph()
    distance, chemin = graphe.shortest_path("lozere", "saclay")

    assert distance == 55
    assert chemin == ["lozere", "ensae", "saclay"]


def test_chemin_graphe_etendu():
    """
    Graphe étendu (question 2) sur small.txt.
    Chemin optimal avec fatigue : lozere -> guichet -> ensae -> saclay
    Coûts : 20 + 15 + 90 = 125
    On appelle shortest_path avec le noeud fictif "fin" comme arrivée.
    """
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_extended_graph()
    distance, chemin = graphe.shortest_path(("lozere", 0), "fin")

    assert distance == 125
    assert chemin == [("lozere", 0), ("guichet", 0), ("ensae", 1), ("saclay", 1), "fin"]
