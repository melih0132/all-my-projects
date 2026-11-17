# On importe les classes nécessaires de la bibliothèque PuLP
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

# ----- 1. Initialisation du modèle -----
# On crée un problème d'optimisation.
# Le premier argument est le nom du problème (pour l'affichage).
# Le second indique si on veut Maximiser (LpMaximize) ou Minimiser (LpMinimize).
model = LpProblem(name="Production_Produits", sense=LpMaximize)

# ----- 2. Définition des variables de décision -----
# On crée les variables x1 et x2.
# LpVariable prend en premier argument le nom de la variable.
# lowBound=0 signifie que la variable doit être >= 0 (c'est notre contrainte de non-négativité).
x1 = LpVariable(name="produit_A", lowBound=0)
x2 = LpVariable(name="produit_B", lowBound=0)

# ----- 3. Ajout de la fonction objectif -----
# On ajoute au modèle l'expression à maximiser.
# C'est la même formule que notre fonction Z.
model += 10 * x1 + 15 * x2, "Benefice_Total"

# ----- 4. Ajout des contraintes -----
# On ajoute chaque contrainte au modèle, avec un nom descriptif.
model += (2 * x1 + 3 * x2 <= 120, "Contrainte_Main_Oeuvre")
model += (3 * x1 + 3 * x2 <= 90, "Contrainte_Matiere_Premiere")

# Affichage du modèle pour vérifier (optionnel mais utile)
print(model)

# ----- 5. Résolution du problème -----
# Le solver va maintenant faire son travail (en utilisant le simplexe ou une autre méthode).
status = model.solve()

# ----- 6. Affichage des résultats -----
print(f"Statut de la solution: {model.status[status]}")
print(f"Bénéfice optimal: {model.objective.value()} €")
print(f"Quantité de produit A (x1) à produire: {x1.value()}")
print(f"Quantité de produit B (x2) à produire: {x2.value()}")
