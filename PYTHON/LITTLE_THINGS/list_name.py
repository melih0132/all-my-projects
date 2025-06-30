import os

# Remplacer ce chemin par celui de ta clé USB (ex: "E:/", "D:/", etc.)
chemin_cle_usb = "E:/"

# Liste pour stocker les noms des morceaux
titres_morceaux = []

# Parcours récursif des fichiers
for dossier_racine, sous_dossiers, fichiers in os.walk(chemin_cle_usb):
    for fichier in fichiers:
        if fichier.lower().endswith(".mp3"):
            titre = os.path.splitext(fichier)[0]  # Supprime l'extension
            titres_morceaux.append(titre)

# Affichage des titres
for titre in titres_morceaux:
    print(titre)
