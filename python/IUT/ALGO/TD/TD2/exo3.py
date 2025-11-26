import random

class Tree:
    def __init__(self, value, children):
        self.value = value
        self.children = children
 
    def count(self):
        total = 1
        for child in self.children:
            total += child.count()
        return total
   
    def __str__(self):
        if self.children:
            children_str = " ".join(str(child) for child in self.children)
            return f"{self.value} ({children_str})"
        return self.value
   
""" html = Tree("body", [
        Tree("h1", [Tree("Pizza", []) ]),
        Tree("article", [Tree(42, []) ]),
        Tree("LD", []),
    ])

print(str(html))
print(html.count()) """

subjects = ["Melih", "Amir", "Tom", "Nathan"]
verbs = ["suce", "chie", "détruit", "baise"]
punctuations = [".", ",", "!", "..."]
conjunctions = ["et", "mais", "ou", "donc", "car"]

def generate_sentence():
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    punctuation = random.choice(punctuations)
    conjunction = random.choice(conjunctions)

    # Générer une phrase avec une liaison
    second_subject = random.choice(subjects)
    second_verb = random.choice(verbs)

    sentence = f"{subject} {verb}{punctuation} {conjunction} {second_subject} {second_verb}{punctuation}"
    return sentence

random_sentence = generate_sentence()
print(random_sentence)