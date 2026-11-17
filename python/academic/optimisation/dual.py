# Import de la bibliothèque
from pulp import LpProblem, LpVariable, LpMaximize

# 1. Initialisation du modèle (Dual)
# On veut maximiser, donc on utilise LpMaximize
model_dual = LpProblem(name="probleme_dual", sense=LpMaximize)

# 2. Définition des variables de décision
# Ce sont y1 et y2, elles doivent être positives.
y1 = LpVariable(name="y1", lowBound=0)
y2 = LpVariable(name="y2", lowBound=0)

# 3. Ajout de la fonction objectif
model_dual += 6 * y1 + 4 * y2, "Fonction_Z"

# 4. Ajout des contraintes
model_dual += (3 * y1 + 1 * y2 <= 6, "Contrainte_1")
model_dual += (1 * y1 + 2 * y2 <= 8, "Contrainte_2")

# 5. Résolution du problème
model_dual.solve()

# 6. Affichage des résultats
print(f"Statut: {model_dual.status[model_dual.status]}")
print(f"Valeur optimale du Dual (Z): {model_dual.objective.value()}")
print(f"Valeur de y1: {y1.value()}")
print(f"Valeur de y2: {y2.value()}")
