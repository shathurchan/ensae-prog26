"""
Module network.py
Contient la classe Network qui représente l'environnement (réseau de routes).
"""
from graph import Graph, GraphImplicit


class Network:
    """
    Représente l'environnement : un réseau de routes orientées avec longueur et fatigue.

    _roads[noeud] = [(voisin, longueur, fatigue), ...]

    start : noeud de départ de la mission
    end   : noeud d'arrivée de la mission
    """

    def __init__(self, roads=None, start=None, end=None):
        self._roads = roads if roads is not None else {}
        self.start = start
        self.end = end

    def __str__(self):
        return str(self._roads)

    @classmethod
    def from_file(cls, filename):
        """
        Charge un réseau depuis un fichier texte.

        Format :
            première ligne  → nb_aretes  noeud_depart  noeud_arrivee
            lignes suivantes → noeud_u  noeud_v  longueur  fatigue
        """
        roads = {}
        with open(filename, "r") as f:
            nb, start, end = f.readline().strip().split()
            for _ in range(int(nb)):
                u, v, longueur, fatigue = f.readline().strip().split()
                roads.setdefault(u, []).append((v, int(longueur), int(fatigue)))
                roads.setdefault(v, [])
        return cls(roads=roads, start=start, end=end)

    def build_simple_graph(self):
        """
        Construit un graphe sans fatigue (question 1 : cas f(e) = 0 pour tout e).
        On ignore les coefficients de fatigue et on garde uniquement les longueurs.
        Retourne un objet Graph.
        """
        edges = {}
        for noeud, voisins in self._roads.items():
            edges[noeud] = [(v, l) for v, l, _ in voisins]
        return Graph(edges)

    def build_extended_graph(self):
        """
        Construit le graphe étendu (question 2 : cas général avec fatigue).

        Chaque noeud du réseau devient un ensemble de copies (noeud, f)
        pour f variant de 0 à F_max, où F_max est la somme de toutes les fatigues.

        Pour chaque arête (u -> v, longueur, fat) du réseau, on ajoute dans le
        graphe étendu l'arête (u, f) -> (v, f + fat) avec coût longueur * (1 + f).

        Un noeud fictif "fin" est relié depuis tous les états (arrivee, f) avec
        coût 0, pour pouvoir appeler shortest_path sans connaître la fatigue finale.

        Retourne un objet Graph.
        """
        # Fatigue maximale atteignable = somme de toutes les fatigues du réseau
        f_max = sum(fat for voisins in self._roads.values() for _, _, fat in voisins)

        edges = {}
        for noeud in self._roads:
            for f in range(f_max + 1):
                edges[(noeud, f)] = []

        for noeud in self._roads:
            for voisin, longueur, fat_arete in self._roads[noeud]:
                for f in range(f_max + 1):
                    nouveau_f = f + fat_arete
                    if nouveau_f <= f_max:
                        cout = longueur * (1 + f)
                        edges[(noeud, f)].append(((voisin, nouveau_f), cout))

        # Noeud fictif "fin" : regroupe tous les états finaux possibles
        edges["fin"] = []
        for f in range(f_max + 1):
            edges[(self.end, f)].append(("fin", 0))

        return Graph(edges)

    def build_implicit_graph(self):
        """
        Construit le graphe implicite (question 3 : optimisation mémoire).

        Contrairement au graphe étendu, on ne crée pas tous les états à l'avance.
        Les voisins sont calculés à la volée dans GraphImplicit.neighbours().
        Retourne un objet GraphImplicit.
        """
        return GraphImplicit(self)
