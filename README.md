## Description

Ce projet implémente des algorithmes de recherche de chemin optimal dans un réseau routier où le coût de déplacement dépend de la fatigue accumulée par l'agent. On part du cas sans fatigue (Dijkstra classique), puis on traite le cas général via un graphe étendu et un graphe implicite, et on propose des améliorations algorithmiques (élagage de Pareto, A*) ainsi qu'une extension avec point de repos.

## Lancer le programme

Depuis la racine du projet :

```bash
python3 code/main.py
```

Le programme demande de choisir un fichier d'exemple et un algorithme, puis affiche la distance minimale et le chemin.

## Lancer les tests

```bash
python3 -m pytest tests/ -v
```
