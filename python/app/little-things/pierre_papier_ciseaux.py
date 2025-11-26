import random

def obtenir_choix_joueur():
    """Demande à l'utilisateur de faire un choix."""
    choix = input("Entrez votre choix (pierre, papier, ciseaux) : ").lower()
    while choix not in ["pierre", "papier", "ciseaux"]:
        choix = input("Choix invalide. Essayez encore (pierre, papier, ciseaux) : ").lower()
    return choix

def obtenir_choix_ordinateur():
    """Génère un choix aléatoire pour l'ordinateur."""
    return random.choice(["pierre", "papier", "ciseaux"])

def determiner_gagnant(choix_joueur, choix_ordinateur):
    """Détermine le gagnant en fonction des règles du jeu."""
    if choix_joueur == choix_ordinateur:
        print("Égalité !")
    elif (choix_joueur == "pierre" and choix_ordinateur == "ciseaux") or \
         (choix_joueur == "papier" and choix_ordinateur == "pierre") or \
         (choix_joueur == "ciseaux" and choix_ordinateur == "papier"):
        print("Vous avez gagné !")
    else:
        print("L'ordinateur a gagné !")

    # Après avoir déterminé le gagnant, demander si l'utilisateur veut rejouer
    obtenir_choix_rejouer()

def obtenir_choix_rejouer():
    """Demande à l'utilisateur s'il veut rejouer."""
    choix = input("Vous voulez rejouer ? (y/n) : ").lower()
    
    while choix not in ["y", "n"]:
        print("Choix invalide. Veuillez entrer 'y' pour oui ou 'n' pour non.")
        choix = input("Vous voulez rejouer ? (y/n) : ").lower()

    if choix == "y":
        jouer()  # Relancer la partie
    elif choix == "n":
        print("Au revoir :)")

def jouer():
    """Fonction principale pour jouer au jeu."""
    choix_joueur = obtenir_choix_joueur()
    choix_ordinateur = obtenir_choix_ordinateur()

    print(f"\nVous avez choisi : {choix_joueur}")
    print(f"L'ordinateur a choisi : {choix_ordinateur}")

    # Déterminer et afficher le résultat
    determiner_gagnant(choix_joueur, choix_ordinateur)

if __name__ == "__main__":
    jouer()
