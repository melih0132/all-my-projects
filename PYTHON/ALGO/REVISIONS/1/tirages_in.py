import random
import time

def tirages_avec_in(n, max_val):
    """
    Génère n nombres uniques aléatoires compris entre 1 et max_val en utilisant 'in'.
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
        if tirage not in nombres:  # Vérification avec 'in'
            nombres.append(tirage)

    elapsed_time = time.time() - start_time

    print(f"Temps d'exécution : {elapsed_time:.4f} sec")
    print(f"Nombre de tirages : {tirages}")

    return nombres

# Exemple d'utilisation
print(tirages_avec_in(24, 24))
