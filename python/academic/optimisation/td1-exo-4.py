from itertools import permutations

def distance(point1, point2):
    return distances[point1][point2]

def total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))

def branch_and_bound():
    min_distance = float('inf')
    min_route = None

    for perm in permutations(clients):
        current_distance = total_distance(('A',) + perm + ('A',))
        if current_distance < min_distance:
            min_distance = current_distance
            min_route = ('A',) + perm + ('A',)

    return min_route, min_distance

# Données du problème
clients = ('B', 'C', 'D', 'E', 'F')
distances = {
    'A': {'B': 10, 'C': 15, 'D': 20, 'E': 25, 'F': 30},
    'B': {'A': 10, 'C': 8, 'D': 12, 'E': 16, 'F': 20},
    'C': {'A': 15, 'B': 8, 'D': 10, 'E': 14, 'F': 18},
    'D': {'A': 20, 'B': 12, 'C': 10, 'E': 6, 'F': 10},
    'E': {'A': 25, 'B': 16, 'C': 14, 'D': 6, 'F': 4},
    'F': {'A': 30, 'B': 20, 'C': 18, 'D': 10, 'E': 4},
}

# Exécution de l'algorithme Branch and Bound
optimal_route, optimal_distance = branch_and_bound()

# Affichage des résultats
print("Solution optimale:")
print("Chemin:", optimal_route)
print("Distance totale:", optimal_distance, "km")
