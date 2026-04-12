import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

from network import Network


def test_structure_graphe_etendu():
    """
    Vérifie que le graphe étendu contient les bons noeuds et arêtes.
    Pour small.txt, f_max = 2+0+1+0 = 3, donc f varie de 0 à 3.
    """
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_extended_graph()

    # Les noeuds (lozere, 0) à (lozere, 3) doivent exister
    for f in range(4):
        assert ("lozere", f) in graphe.edges

    # Depuis (lozere, 0) : arête vers (ensae, 2) coût 10*(1+0)=10
    assert (("ensae", 2), 10) in graphe.edges[("lozere", 0)]
    # Depuis (lozere, 0) : arête vers (guichet, 0) coût 20*(1+0)=20
    assert (("guichet", 0), 20) in graphe.edges[("lozere", 0)]

    # Le noeud fictif "fin" doit exister
    assert "fin" in graphe.edges

    # Tous les états finaux (saclay, f) pointent vers "fin"
    for f in range(4):
        assert ("fin", 0) in graphe.edges[("saclay", f)]


def test_distance_graphe_etendu():
    """
    Vérifie que shortest_path donne la bonne distance sur small.txt.
    Chemin optimal : lozere -> guichet -> ensae -> saclay -> fin
    Coûts : 20 + 15 + 90 + 0 = 125
    """
    reseau = Network.from_file(NET_DIR / "small.txt")
    graphe = reseau.build_extended_graph()
    distance, chemin = graphe.shortest_path(("lozere", 0), "fin")

    assert distance == 125
    assert chemin[0] == ("lozere", 0)
    assert chemin[-1] == "fin"
    # Le noeud juste avant "fin" doit être (saclay, 1)
    assert chemin[-2] == ("saclay", 1)
