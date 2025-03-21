import random
import time

def est_dans_liste(valeur, liste):
    """ Vérifie manuellement si une valeur est déjà dans la liste. """
    for elem in liste:
        if elem == valeur:
            return True
    return False

def tirages_sans_in(n, max_val):
    """
    Génère n nombres uniques aléatoires compris entre 1 et max_val sans utiliser 'in'.
    Mesure aussi le temps d'exécution.
    """
    if n > max_val:
        raise ValueError("Impossible de générer plus de nombres uniques que la plage disponible.")

    start_time = time.time()

    nombres = []
    tirages = 0

    while len(nombres) < n:
        tirage = random.randint(1, max_val)
        tirages += 1
        if not est_dans_liste(tirage, nombres):  # Vérification manuelle
            nombres.append(tirage)

    elapsed_time = time.time() - start_time

    print(f"Temps d'exécution : {elapsed_time:.4f} sec")
    print(f"Nombre de tirages : {tirages}")

    return nombres

# Exemple d'utilisation
print(tirages_sans_in(24, 24))
