from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Capacités des serveurs
capacites = {'A': 100, 'B': 150, 'C': 120, 'D': 200}

# Besoins en capacité de traitement des tâches
besoins = {'1': 30, '2': 40, '3': 20, '4': 60, '5': 50}

# Consommation d'énergie par unité de traitement pour chaque serveur
consommation_energie = {'A': 2, 'B': 2.5, 'C': 2, 'D': 3}

# Temps d'exécution par unité de traitement pour chaque tâche
temps_execution = {'1': 1, '2': 1, '3': 1, '4': 1, '5': 1}

# Limite de temps d'exécution total
limite_temps_execution = 4

# Création du problème d'optimisation
probleme = LpProblem("Allocation_Taches", LpMinimize)

# Variables de décision
allocation = LpVariable.dicts("allocation", ((i, j) for i in capacites for j in besoins), 0, 1, LpMinimize)
temps_total_execution = LpVariable("temps_total_execution", 0, limite_temps_execution, LpMinimize)

# Fonction objectif : minimiser la consommation totale d'énergie
probleme += lpSum(allocation[i, j] * consommation_energie[i] * besoins[j] for i in capacites for j in besoins)

# Contraintes de capacité des serveurs
for i in capacites:
    probleme += lpSum(allocation[i, j] * besoins[j] for j in besoins) <= capacites[i]

# Contraintes d'allocation des tâches (une tâche est attribuée à un seul serveur)
for j in besoins:
    probleme += lpSum(allocation[i, j] for i in capacites) == 1

# Contrainte sur le temps d'exécution total
probleme += lpSum(allocation[i, j] * temps_execution[j] for i in capacites for j in besoins) <= temps_total_execution

# Résolution du problème
probleme.solve()

# Affichage de la solution
#print("Status:", LpProblem.status[probleme.status])

if probleme.status == 1:  # 1 correspond à Optimal dans PuLP
    for i in capacites:
        for j in besoins:
            if allocation[i, j].value() > 0.5:  # Utiliser une valeur seuil pour traiter les erreurs d'arrondi
                print(f"Assigner la tâche {j} au serveur {i}")
    print("Consommation totale d'énergie:", round(probleme.objective.value(), 2), "Wh")
    print("Temps d'exécution total des tâches:", round(temps_total_execution.value(), 2), "unités de temps")
else:
    print("Aucune solution optimale trouvée.")
