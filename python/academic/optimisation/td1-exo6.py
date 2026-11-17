from pulp import *

# Create the problem variable
prob = LpProblem("Meubles production", LpMaximize)

# Create problem variables
x = LpVariable("x", 0, None, cat='Continious')
y = LpVariable("y", 0, None, cat='Continious')
z = LpVariable("z", 0, None, cat='Continious')

# Add objective function
prob += 120*x + 165*y, "Z"

# Add constraints
prob += 3*x + 3*y <= 180
prob += x + 2*y <= 120
prob += 2*x + 3*y <= 80

# Solve the problem
status = prob.solve()

# Print the solution
print(f'Status: {LpStatus[status]}')
print(f'x = {x.value()}, y = {y.value()} => Z = {value(prob.objective)}')