"""
Module graph.py
Contient les classes Graph, GraphImplicit et RestedGraph.
"""
import heapq
from itertools import count


def est_pareto_domine(noeud, temps, fatigue, non_domines):
    """
    Elagage de Pareto : vérifie si un état (noeud, temps, fatigue) est dominé.

    Un état (t, f) est dominé s'il existe un état déjà connu (t', f') tel que
    t' <= t et f' <= f avec au moins une inégalité stricte.
    Dans ce cas, l'état ne peut pas mener à une solution optimale et on l'ignore.

    Met aussi à jour non_domines en supprimant les états devenus dominés.
    Retourne True si l'état est dominé, False sinon.
    """
    etats_connus = non_domines.get(noeud, [])

    for t_prec, f_prec in etats_connus:
        if t_prec <= temps and f_prec <= fatigue and (t_prec < temps or f_prec < fatigue):
            return True  # dominé, on ignore cet état

    # Supprimer les anciens états dominés par le nouvel état
    non_domines[noeud] = [
        (t, f) for t, f in etats_connus
        if not (temps <= t and fatigue <= f and (temps < t or fatigue < f))
    ]
    non_domines[noeud].append((temps, fatigue))
    return False


class Graph:
    """
    Graphe orienté pondéré sans fatigue.
    Utilisé pour la question 1 (cas sans fatigue) et la question 2 (graphe étendu).

    edges[noeud] = [(voisin, poids), ...]
    """

    def __init__(self, edges):
        self.edges = edges

    def neighbours(self, noeud):
        """Retourne la liste des voisins d'un noeud et leur poids."""
        return self.edges.get(noeud, [])

    def __str__(self):
        return str(self.edges)

    def shortest_path(self, depart, arrivee):
        """
        Algorithme de Dijkstra : chemin de poids minimal entre depart et arrivee.

        Retourne (distance_min, chemin).
        Si aucun chemin n'existe, retourne (inf, []).

        Le compteur cpt évite les comparaisons entre noeuds de types différents
        (ex. chaînes et tuples) quand deux distances sont égales dans le tas.
        """
        cpt = count()
        dist = {depart: 0}
        parent = {depart: None}
        tas = [(0, next(cpt), depart)]
        visites = set()

        while tas:
            d, _, noeud = heapq.heappop(tas)
            if noeud in visites:
                continue
            visites.add(noeud)

            if noeud == arrivee:
                break

            for voisin, poids in self.neighbours(noeud):
                nouvelle_dist = d + poids
                if voisin not in dist or nouvelle_dist < dist[voisin]:
                    dist[voisin] = nouvelle_dist
                    parent[voisin] = noeud
                    heapq.heappush(tas, (nouvelle_dist, next(cpt), voisin))

        if arrivee not in dist:
            return float("inf"), []

        # Reconstruction du chemin depuis l'arrivée jusqu'au départ
        chemin = []
        noeud = arrivee
        while noeud is not None:
            chemin.append(noeud)
            noeud = parent[noeud]
        chemin.reverse()
        return dist[arrivee], chemin


class GraphImplicit(Graph):
    """
    Graphe implicite avec fatigue : on ne construit pas explicitement tous les noeuds,
    les voisins sont calculés à la volée depuis le réseau sous-jacent.

    Un état est un couple (noeud, fatigue_cumulée).
    Coût d'une arête (u -> v) depuis l'état (u, f) : longueur * (1 + f).

    Plus efficace que le graphe étendu car on évite d'énumérer
    tous les états (noeud, fatigue) à l'avance.
    """

    def __init__(self, reseau):
        self.reseau = reseau
        self.min_dist = {}  # rempli par precalculer_distances(), pour l'heuristique A*

    def neighbours(self, etat):
        """
        Voisins de l'état (noeud, fatigue).
        Retourne une liste de ((voisin, nouvelle_fatigue), coût).
        """
        noeud, fatigue = etat
        voisins = []
        for (suivant, longueur, fatigue_arete) in self.reseau._roads.get(noeud, []):
            nouvelle_fatigue = fatigue + fatigue_arete
            cout = longueur * (1 + fatigue)
            voisins.append(((suivant, nouvelle_fatigue), cout))
        return voisins

    def precalculer_distances(self, destination):
        """
        Dijkstra inversé : calcule la distance minimale (sans fatigue) de chaque
        noeud vers la destination. Sert d'heuristique pour A*.

        On construit d'abord le graphe inversé (toutes les arêtes à l'envers),
        puis on fait Dijkstra depuis la destination.
        """
        graphe_inv = {}
        for u, voisins in self.reseau._roads.items():
            for v, longueur, _ in voisins:
                graphe_inv.setdefault(v, []).append((u, longueur))

        self.min_dist = {destination: 0}
        tas = [(0, destination)]
        visites = set()

        while tas:
            d, noeud = heapq.heappop(tas)
            if noeud in visites:
                continue
            visites.add(noeud)
            for pred, longueur in graphe_inv.get(noeud, []):
                nd = d + longueur
                if pred not in self.min_dist or nd < self.min_dist[pred]:
                    self.min_dist[pred] = nd
                    heapq.heappush(tas, (nd, pred))

    def _heuristique(self, etat):
        """
        Heuristique admissible pour A* :
            h(noeud, f) = distance_min_restante * (1 + f)

        Elle sous-estime toujours le vrai coût car la fatigue ne peut qu'augmenter.
        """
        noeud, fatigue = etat
        return self.min_dist.get(noeud, float("inf")) * (1 + fatigue)

    def shortest_path(self, depart, arrivee, avec_astar=False, avec_elagage=False):
        """
        Dijkstra (ou A*) sur le graphe implicite avec fatigue.

        depart, arrivee : noms des noeuds (chaînes de caractères)
        avec_astar      : active l'heuristique A* (nécessite d'appeler
                          precalculer_distances() avant)
        avec_elagage    : active l'élagage de Pareto

        L'état initial est (depart, 0) : on démarre avec fatigue = 0.
        On s'arrête dès qu'on dépile un état dont le noeud vaut arrivee
        (propriété de Dijkstra : le premier dépilage est optimal).

        Retourne (distance_min, chemin) où chemin est une liste d'états (noeud, fatigue).
        """
        etat_init = (depart, 0)
        cpt = count()
        dist = {etat_init: 0}
        parent = {etat_init: None}
        tas = [(0, next(cpt), etat_init)]
        visites = set()
        non_domines = {}

        etat_arrivee = None

        while tas:
            _, _, etat = heapq.heappop(tas)
            if etat in visites:
                continue
            visites.add(etat)

            noeud, fatigue = etat
            if noeud == arrivee:
                etat_arrivee = etat
                break

            for etat_suivant, cout in self.neighbours(etat):
                nouveau_temps = dist[etat] + cout
                noeud_suiv, fatigue_suiv = etat_suivant

                if avec_elagage and est_pareto_domine(noeud_suiv, nouveau_temps, fatigue_suiv, non_domines):
                    continue

                if etat_suivant not in dist or nouveau_temps < dist[etat_suivant]:
                    dist[etat_suivant] = nouveau_temps
                    parent[etat_suivant] = etat
                    h = self._heuristique(etat_suivant) if avec_astar else 0
                    heapq.heappush(tas, (nouveau_temps + h, next(cpt), etat_suivant))

        if etat_arrivee is None:
            return float("inf"), []

        # Reconstruction du chemin
        chemin = []
        etat = etat_arrivee
        while etat is not None:
            chemin.append(etat)
            etat = parent[etat]
        chemin.reverse()
        return dist[etat_arrivee], chemin


class RestedGraph(GraphImplicit):
    """
    Extension : graphe implicite avec la possibilité de faire UNE pause.
    La pause est gratuite (coût = 0) et remet la fatigue à zéro.
    Elle ne peut être utilisée qu'une seule fois.

    Un état est un triplet (noeud, fatigue, repos_utilise) où repos_utilise ∈ {0, 1}.
    """

    def neighbours(self, etat):
        """
        Voisins normaux, plus l'option de faire une pause sur place
        si elle n'a pas encore été utilisée.
        """
        noeud, fatigue, repos_utilise = etat
        voisins = []

        for (suivant, longueur, fatigue_arete) in self.reseau._roads.get(noeud, []):
            nouvelle_fatigue = fatigue + fatigue_arete
            cout = longueur * (1 + fatigue)
            voisins.append(((suivant, nouvelle_fatigue, repos_utilise), cout))

        # Option : faire une pause ici (fatigue -> 0, coût = 0)
        if repos_utilise == 0:
            voisins.append(((noeud, 0, 1), 0))

        return voisins

    def _heuristique(self, etat):
        noeud, fatigue, _ = etat
        return self.min_dist.get(noeud, float("inf")) * (1 + fatigue)

    def noeud_pause(self, chemin):
        """Retourne le noeud où la pause a été effectuée dans le chemin."""
        for i in range(1, len(chemin)):
            _, _, repos_avant = chemin[i - 1]
            _, _, repos_apres = chemin[i]
            if repos_avant == 0 and repos_apres == 1:
                return chemin[i - 1][0]
        return None

    def shortest_path(self, depart, arrivee, avec_astar=False):
        """
        Dijkstra sur le graphe avec pause.
        Retourne (distance_min, chemin) où chemin est une liste
        d'états (noeud, fatigue, repos_utilise).
        """
        etat_init = (depart, 0, 0)
        cpt = count()
        dist = {etat_init: 0}
        parent = {etat_init: None}
        tas = [(0, next(cpt), etat_init)]
        visites = set()

        etat_arrivee = None

        while tas:
            _, _, etat = heapq.heappop(tas)
            if etat in visites:
                continue
            visites.add(etat)

            noeud, fatigue, repos_utilise = etat
            if noeud == arrivee:
                etat_arrivee = etat
                break

            for etat_suivant, cout in self.neighbours(etat):
                nouveau_temps = dist[etat] + cout
                if etat_suivant not in dist or nouveau_temps < dist[etat_suivant]:
                    dist[etat_suivant] = nouveau_temps
                    parent[etat_suivant] = etat
                    h = self._heuristique(etat_suivant) if avec_astar else 0
                    heapq.heappush(tas, (nouveau_temps + h, next(cpt), etat_suivant))

        if etat_arrivee is None:
            return float("inf"), []

        chemin = []
        etat = etat_arrivee
        while etat is not None:
            chemin.append(etat)
            etat = parent[etat]
        chemin.reverse()
        return dist[etat_arrivee], chemin
