!pip install pulp
from pulp import *

# Create the problem variable
prob = LpProblem("Meubles production", LpMaximize)

# Create problem variables
x = LpVariable("x", 0, None, cat='Integer') # Nombre de chaises produites
y = LpVariable("y", 0, None, cat='Integer') # Nombre de tables produites

# Add objective function
prob += 10*x + 20*y, "Z"

# Add constraints
prob += 2*x + 4*y <= 8 # nombre limité d'heures de travail disponibles
prob += 3*x + 5*y <= 15 # stock limité de matiere premiere

# Solve the problem
status = prob.solve()

# Print the solution
print(f'Status: {LpStatus[status]}')
print(f'x = {x.value()}, y = {y.value()} => Z = {value(prob.objective)}')