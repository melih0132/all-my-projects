from pulp import LpMaximize, LpProblem, LpVariable

# Créer un problème de maximisation
prob = LpProblem("Selection_de_Projets", LpMaximize)

# Variables binaires pour les projets
projets = range(1, 6)
x = LpVariable.dicts("Projet", projets, cat="Binary")

# Coûts et profits des projets
couts = {1: 2000, 2: 3500, 3: 1200, 4: 4000, 5: 2800}
profits = {1: 5000, 2: 8000, 3: 3000, 4: 9000, 5: 7000}

# Fonction objectif
prob += sum(profits[i] * x[i] for i in projets), "Profit_Total"

# Contrainte budgétaire
prob += sum(couts[i] * x[i] for i in projets) <= 10000, "Contrainte_Budget"

# Résoudre le problème
prob.solve()

# Afficher la solution
#print("Status:", LpProblem.status[prob.status])
print("Projets sélectionnés:")
for i in projets:
    if x[i].value() == 1:
        print(f"Projet {i} (Coût : {couts[i]}, Profit : {profits[i]})")
print("Profit Total:", sum(profits[i] for i in projets if x[i].value() == 1))