#! pip install pulp
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Capacités des serveurs
capacites = {'A': 100, 'B': 150, 'C': 120, 'D': 200}

# Besoins en capacité de traitement des tâches
besoins = {'1': 30, '2': 40, '3': 20, '4': 60, '5': 50}

# Consommation d'énergie par unité de traitement pour chaque serveur
consommation_energie = {'A': 2, 'B': 2.5, 'C': 2, 'D': 3}

# Création du problème d'optimisation
probleme = LpProblem("Allocation_Taches", LpMinimize)

# Variables de décision
allocation = LpVariable.dicts("allocation", ((i, j) for i in capacites for j in besoins), 0, 1, LpMinimize)

# Fonction objectif : minimiser la consommation totale d'énergie
probleme += lpSum(allocation[i, j] * consommation_energie[i] * besoins[j] for i in capacites for j in besoins)

# Contraintes de capacité des serveurs
for i in capacites:
    probleme += lpSum(allocation[i, j] * besoins[j] for j in besoins) <= capacites[i]

# Contraintes d'allocation des tâches (une tâche est attribuée à un seul serveur)
for j in besoins:
    probleme += lpSum(allocation[i, j] for i in capacites) == 1

# Résolution du problème
probleme.solve()

# Affichage de la solution
if probleme.status == 1:  # 1 correspond à Optimal dans PuLP
    for i in capacites:
        for j in besoins:
            if allocation[i, j].value() > 0.5:
                print(f"Assigner la tâche {j} au serveur {i}")
    print("Consommation totale d'énergie:", round(probleme.objective.value(), 2), "Wh")
else:
    print("Aucune solution optimale trouvée.")
