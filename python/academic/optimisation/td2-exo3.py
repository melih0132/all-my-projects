from pulp import LpMaximize, LpProblem, LpVariable

# Créer un problème de maximisation linéaire
probleme = LpProblem("Maximisation_Taches", LpMaximize)

# Définir les variables de décision
xA = LpVariable("xA", lowBound=0)  # Quantité allouée de la tâche A
xB = LpVariable("xB", lowBound=0)  # Quantité allouée de la tâche B
xC = LpVariable("xC", lowBound=0)  # Quantité allouée de la tâche C

# Définir la fonction objectif
probleme += xA + xB + xC, "Maximiser_Taches"

# Ajouter les contraintes
probleme += 2*xA + xB + 3*xC <= 5
probleme += 3*xA + 2*xB + xC <= 5
probleme += xA + 2*xB + 4*xC <= 15

# Résoudre le problème avec l'algorithme Simplex
probleme.solve()

# Afficher les résultats
#print("Statut:", LpProblem.status[probleme.status])
print("Quantité allouée de la tâche A =", xA.varValue)
print("Quantité allouée de la tâche B =", xB.varValue)
print("Quantité allouée de la tâche C =", xC.varValue)
print("Nombre de tâches maximisé =", probleme.objective.value())