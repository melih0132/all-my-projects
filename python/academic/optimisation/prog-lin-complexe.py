from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Données
capacities = [120, 150, 180]  # Capacité des entrepôts
demands = [50, 60, 70, 100]  # Demande des magasins
costs = [  # Coûts de transport
    [4, 6, 9, 8],
    [5, 4, 8, 7],
    [6, 5, 7, 6]
]

# Modèle
model = LpProblem("Transport_Optimization", LpMinimize)

# Variables de décision
x = [[LpVariable(f"x_{i+1}_{j+1}", lowBound=0) for j in range(4)] for i in range(3)]

# Fonction objectif
model += lpSum(costs[i][j] * x[i][j] for i in range(3) for j in range(4))

# Contraintes de capacité des entrepôts
for i in range(3):
    model += lpSum(x[i][j] for j in range(4)) <= capacities[i], f"Capacity_E{i+1}"

# Contraintes de demande des magasins
for j in range(4):
    model += lpSum(x[i][j] for i in range(3)) == demands[j], f"Demand_M{j+1}"

# Résolution
model.solve()

# Résultats
print("Statut :", model.status)
print("Coût total optimal :", model.objective.value())
for i in range(3):
    for j in range(4):
        print(f"x_{i+1}_{j+1} = {x[i][j].value()} unités")
