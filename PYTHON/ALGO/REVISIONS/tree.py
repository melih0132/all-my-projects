class Tree:
    def __init__(self, value):
        """ Initialise un nœud avec une valeur et une liste de sous-arbres. """
        self.value = value
        self.subTrees = []

    def add_subtree(self, subtree):
        """ Ajoute un sous-arbre au nœud courant. """
        self.subTrees.append(subtree)

def count(tree):
    """ Retourne le nombre total de nœuds dans l'arbre. """
    if not tree:
        return 0
    return 1 + sum(count(subtree) for subtree in tree.subTrees)

def depth(tree):
    """ Retourne la profondeur de l'arbre. """
    if not tree or not tree.subTrees:
        return 1
    return 1 + max(depth(subtree) for subtree in tree.subTrees)

def tree_list(tree, func):
    """ Applique une fonction à chaque valeur et retourne une liste des résultats. """
    if not tree:
        return []
    return [func(tree.value)] + [item for subtree in tree.subTrees for item in tree_list(subtree, func)]

# Exemple d'utilisation
if __name__ == "__main__":
    root = Tree(1)
    child1 = Tree(2)
    child2 = Tree(3)
    child1.add_subtree(Tree(4))
    child1.add_subtree(Tree(5))
    child2.add_subtree(Tree(6))
    
    root.add_subtree(child1)
    root.add_subtree(child2)

    print(f"Nombre de nœuds : {count(root)}")
    print(f"Profondeur de l'arbre : {depth(root)}")
    print(f"Valeurs multipliées par 2 : {tree_list(root, lambda x: x * 2)}")
