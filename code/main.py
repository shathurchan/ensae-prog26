"""
main.py
Point d'entrée du programme : charge un réseau, lance un algorithme de plus
court chemin, et propose de trouver le point de repos optimal (extension).
"""
import time
from network import Network
from graph import RestedGraph

# Fichiers d'exemples disponibles
fichiers = [
    "examples/small.txt",
    "examples/medium-nofatigue.txt",
    "examples/medium-smallfatigue.txt",
    "examples/medium-largefatigue.txt",
    "examples/large-nofatigue.txt",
    "examples/large-smallfatigue.txt",
    "examples/large-largefatigue.txt",
]

print("=== Chemin optimal avec fatigue ===\n")
print("Fichiers disponibles :")
for i, f in enumerate(fichiers):
    print(f"  {i} : {f}")
num = int(input("\nChoisissez un fichier (0-6) : "))
reseau = Network.from_file(fichiers[num])

print("\nAlgorithme :")
print("  1. Dijkstra")
print("  2. A*")
print("  3. Dijkstra + élagage de Pareto")
print("  4. A* + élagage de Pareto")
choix = int(input("Votre choix (1-4) : "))

# On utilise le graphe implicite (plus efficace que le graphe étendu)
graphe = reseau.build_implicit_graph()
graphe.precalculer_distances(reseau.end)

avec_astar    = choix in (2, 4)
avec_elagage  = choix in (3, 4)

debut = time.time()
distance, chemin = graphe.shortest_path(
    reseau.start, reseau.end,
    avec_astar=avec_astar,
    avec_elagage=avec_elagage
)
fin = time.time()

print(f"\nDistance minimale : {distance}")
print(f"Chemin : {chemin}")
print(f"Temps de calcul : {fin - debut:.4f} s")

# --- Extension : point de repos optimal ---
rep = input("\nVoulez-vous trouver le meilleur endroit pour faire une pause ? (o/n) : ")
if rep == "o":
    graphe_repos = RestedGraph(reseau)
    graphe_repos.precalculer_distances(reseau.end)

    debut = time.time()
    dist_repos, chemin_repos = graphe_repos.shortest_path(
        reseau.start, reseau.end, avec_astar=True
    )
    fin = time.time()

    pause = graphe_repos.noeud_pause(chemin_repos)
    print(f"\nDistance avec pause : {dist_repos}")
    print(f"Meilleur endroit pour la pause : {pause}")
    print(f"Temps de calcul : {fin - debut:.4f} s")
