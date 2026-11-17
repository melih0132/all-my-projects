#! pip install pulp
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Générer un tableau aléatoire de 100 personnes et 100 tâches avec des coûts aléatoires
num_people = 10000
num_tasks = 10000
cost_matrix = np.random.randint(1, 10001, size=(num_people, num_tasks))
# Imprimer le tableau généré
print("Tableau aléatoire de coûts de formation :")
print(cost_matrix)


num_people, num_tasks = len(cost_matrix), len(cost_matrix[0])

# Création du problème de programmation linéaire
prob = LpProblem("Assignment Problem", LpMinimize)

# Variables de décision
x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(num_tasks)] for i in range(num_people)]

# Fonction objectif
prob += lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_people) for j in range(num_tasks))

# Contraintes
for i in range(num_people):
    prob += lpSum(x[i][j] for j in range(num_tasks)) == 1

for j in range(num_tasks):
    prob += lpSum(x[i][j] for i in range(num_people)) == 1

# Résolution du problème
prob.solve()

# Affichage des résultats
#print("Statut de résolution:", prob.LpStatus[prob.status])
print("Coût total de formation:", round(prob.objective.value(), 2))

# Affichage de l'affectation optimale
assignment = {(i, j): int(x[i][j].value()) for i in range(num_people) for j in range(num_tasks)}
print("Affectation optimale:")
for i in range(num_people):
    for j in range(num_tasks):
        if assignment[(i, j)] == 1:
            print(f"Personne {i+1} -> Tâche {j+1}")
