"""
main.py
Point d'entrée du programme : charge un réseau et lance un algorithme de plus
court chemin.
"""
import time
from network import Network

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
