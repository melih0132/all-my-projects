import random

def generate_phrase(tree):
    """ Parcours l'arbre et génère une phrase en choisissant aléatoirement les branches. """
    if isinstance(tree, str):
        return tree
    return " ".join(generate_phrase(random.choice(tree)) for tree in tree)

# Arbre syntaxique pour générer des phrases
syntaxe = [
    [["Le", "Un"], ["chat", "chien", "robot"], ["mange", "court", "dort"], ["rapidement", "joyeusement", "lentement"]],
    [["Cette", "Une"], ["maison", "voiture", "idée"], ["est", "semble"], ["belle", "étrange", "intéressante"]]
]

# Génération de phrases aléatoires
if __name__ == "__main__":
    for _ in range(5):  # Générer 5 phrases
        print(generate_phrase(random.choice(syntaxe)))
