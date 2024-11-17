# Modules
import math
import requests

# Saisie utilisateur
nom = input("Entrez votre nom : ")
âge = int(input("Entrez votre âge : "))

# Affichage de base
print(f"Nom: {nom}, Âge: {âge}")

# Structures de contrôle
if âge < 18:
    print("Mineur")
else:
    print("Majeur")

# Boucle for
for i in range(5):
    print(f"Compteur: {i}")

# Boucle while
compteur = 0
while compteur < 5:
    print(f"Compteur while: {compteur}")
    compteur += 1

# Listes
fruits = ["pomme", "banane", "cerise"]
fruits.append("orange")
print(f"Fruits: {fruits}")

# Tuples (immuables)
coordonnées = (10.0, 20.0)

# Dictionnaires
étudiant = {"nom": nom, "âge": âge}
print(f"Nom de l'étudiant: {étudiant['nom']}")

# Fonctions
def saluer(nom):
    return f"Bonjour, {nom} !"

print(saluer(nom))

# Compréhensions de liste
carrés = [x**2 for x in range(10)]
print(f"Carrés: {carrés}")

# Gestion des exceptions
try:
    résultat = 10 / 0
except ZeroDivisionError:
    print("Erreur: Division par zéro")

# Classes et objets
class Personne:
    def __init__(self, nom, âge):
        self.nom = nom
        self.âge = âge

    def se_presenter(self):
        return f"Je m'appelle {self.nom} et j'ai {self.âge} ans."

p = Personne(nom, âge)
print(p.se_presenter())

# Modules
print(f"Pi: {math.pi}")

# Fichiers
with open("exemple.txt", "w") as fichier:
    fichier.write("Bonjour, monde!")

with open("exemple.txt", "r") as fichier:
    contenu = fichier.read()
    print(contenu)

# Modules externes
response = requests.get("https://api.github.com")
print(response.status_code)

# Expressions lambda
addition = lambda x, y: x + y
print(addition(3, 5))

# Décorateurs
def mon_decorateur(fonction):
    def fonction_modifiée():
        print("Avant l'appel")
        fonction()
        print("Après l'appel")
    return fonction_modifiée

@mon_decorateur
def dire_bonjour():
    print("Bonjour!")

dire_bonjour()

# Générateurs
def compte():
    i = 0
    while i < 5:
        yield i
        i += 1

for nombre in compte():
    print(nombre)

# Programmation orientée objet avancée
class Animal:
    def parler(self):
        pass

class Chien(Animal):
    def parler(self):
        return "Woof!"

class Chat(Animal):
    def parler(self):
        return "Meow!"

animaux = [Chien(), Chat()]

for animal in animaux:
    print(animal.parler())

# Encapsulation, Héritage, et Polymorphisme
class Animal:
    def __init__(self, nom):
        self.__nom = nom  # Attribut privé (encapsulation)

    def parler(self):
        pass

    # Accesseur pour l'attribut privé
    def get_nom(self):
        return self.__nom

    # Mutateur pour l'attribut privé
    def set_nom(self, nom):
        self.__nom = nom

class Chien(Animal):
    def parler(self):
        return f"{self.get_nom()} dit: Woof!"

class Chat(Animal):
    def parler(self):
        return f"{self.get_nom()} dit: Meow!"

# Héritage multiple : un animal magique peut voler
class AnimalMagique:
    def voler(self):
        return "Je peux voler!"

class Dragon(Animal, AnimalMagique):  # Héritage multiple
    def parler(self):
        return f"{self.get_nom()} dit: Roar!"

# Méthode et attributs statiques
class Zoo:
    nombre_animaux = 0  # Attribut statique

    def __init__(self, nom):
        self.nom = nom
        self.animaux = []
        Zoo.nombre_animaux += 1

    def ajouter_animal(self, animal):
        self.animaux.append(animal)

    @staticmethod
    def nombre_de_zoos():
        return f"Il y a {Zoo.nombre_animaux} zoos."

# Surcharge d'opérateurs (ex. ajouter des animaux à un zoo avec "+")
    def __add__(self, animal):
        self.ajouter_animal(animal)
        return self

# Composition : un zoo a plusieurs animaux
zoo1 = Zoo("Parc Animalier")
chien = Chien("Buddy")
chat = Chat("Mimi")
dragon = Dragon("Smaug")

# Ajout d'animaux via la surcharge d'opérateurs
zoo1 + chien + chat + dragon

# Afficher les animaux et leurs sons
for animal in zoo1.animaux:
    print(animal.parler())

# Le dragon peut voler grâce à l'héritage multiple
print(dragon.voler())

# Afficher le nombre de zoos créés
print(Zoo.nombre_de_zoos())
