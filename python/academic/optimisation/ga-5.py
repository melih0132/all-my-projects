import numpy as np
import random

import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Générer un tableau aléatoire de 100 personnes et 100 tâches avec des coûts aléatoires
num_people = 10000
num_tasks = 10000
cost_matrix = np.random.randint(1, 10001, size=(num_people, num_tasks))

# Imprimer le tableau généré
print("Tableau aléatoire de coûts de formation :")
print(cost_matrix)




# Paramètres de l'algorithme génétique
population_size = 50
num_generations = 1000
mutation_rate = 0.02

def initialize_population(population_size):
    return [list(np.random.permutation(len(cost_matrix[0]))) for _ in range(population_size)]

def calculate_fitness(individual):
    assignment = np.zeros_like(cost_matrix)
    for i in range(len(individual)):
        assignment[i, individual[i]] = 1
    total_cost = np.sum(cost_matrix * assignment)
    return -total_cost  # Maximiser le fitness revient à minimiser le coût

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

def mutate(individual):
    mutated_individual = individual.copy()
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(mutated_individual) - 1)
            mutated_individual[i], mutated_individual[mutation_point] = (
                mutated_individual[mutation_point], mutated_individual[i]
            )
    return mutated_individual

# Algorithme génétique
population = initialize_population(population_size)

for generation in range(num_generations):
    fitness = [calculate_fitness(ind) for ind in population]

    # Sélection des meilleurs individus
    selected_indices = np.argsort(fitness)[-population_size:]
    selected_population = [population[i] for i in selected_indices]

    # Création d'une nouvelle population par croisement et mutation
    new_population = []

    for _ in range(population_size // 2):
        parent1, parent2 = random.sample(selected_population, 2)
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([mutate(child1), mutate(child2)])

    population = new_population

# Affichage de la solution optimale
best_solution_index = np.argmax([calculate_fitness(ind) for ind in population])
best_solution = population[best_solution_index]
best_cost = -calculate_fitness(best_solution)

print("Affectation optimale:")
print(np.array(best_solution) + 1)  # +1 pour correspondre à l'indexation à partir de 1
print("Coût total de formation:", best_cost)
