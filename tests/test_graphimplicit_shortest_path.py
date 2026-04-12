import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

from network import Network


def test_chemin_graphe_implicite():
    """
    Graphe implicite (question 3) sur small.txt.
    Doit donner le même résultat que le graphe étendu.
    Chemin optimal : lozere -> guichet -> ensae -> saclay
    Distance : 125
    """
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_implicit_graph()
    distance, chemin = graphe.shortest_path("lozere", "saclay")

    assert distance == 125
    assert chemin == [("lozere", 0), ("guichet", 0), ("ensae", 1), ("saclay", 1)]


def test_astar_meme_resultat():
    """A* doit donner la même distance que Dijkstra."""
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_implicit_graph()
    graphe.precalculer_distances(reseau.end)

    dist_dijkstra, _ = graphe.shortest_path("lozere", "saclay")
    dist_astar, _    = graphe.shortest_path("lozere", "saclay", avec_astar=True)

    assert dist_dijkstra == dist_astar == 125


def test_elagage_meme_resultat():
    """L'élagage de Pareto doit donner la même distance que Dijkstra."""
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_implicit_graph()

    dist_sans, _ = graphe.shortest_path("lozere", "saclay")
    dist_avec, _ = graphe.shortest_path("lozere", "saclay", avec_elagage=True)

    assert dist_sans == dist_avec == 125
