# Liste pour stocker les tâches
taches = []

def ajouter_tache(tache):
    """Ajoute une nouvelle tâche à la liste."""
    taches.append({"tache": tache, "fait": False})
    print(f"Tâche '{tache}' ajoutée.")

def afficher_taches():
    """Affiche toutes les tâches avec leur statut (fait ou non)."""
    if not taches:
        print("Aucune tâche à afficher.")
        return
    print("\nListe des tâches :")
    for i, tache in enumerate(taches, start=1):
        statut = "✓" if tache["fait"] else "✗"
        print(f"{i}. {tache['tache']} [{statut}]")

def marquer_comme_faite(index):
    """Marque une tâche comme faite en fonction de son index."""
    if 0 < index <= len(taches):
        taches[index - 1]["fait"] = True
        print(f"Tâche '{taches[index - 1]['tache']}' marquée comme faite.")
    else:
        print("Index invalide.")

def menu():
    """Affiche le menu pour interagir avec le gestionnaire."""
    while True:
        print("\nOptions :")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Marquer une tâche comme faite")
        print("4. Quitter")

        choix = input("Choisissez une option : ")

        if choix == '1':
            tache = input("Entrez la tâche à ajouter : ")
            ajouter_tache(tache)
        elif choix == '2':
            afficher_taches()
        elif choix == '3':
            try:
                index = int(input("Entrez le numéro de la tâche à marquer comme faite : "))
                marquer_comme_faite(index)
            except ValueError:
                print("Veuillez entrer un numéro valide.")
        elif choix == '4':
            print("Au revoir !")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()