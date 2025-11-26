

# Notation polonaise inversée :

# * 3 + 5 2 = 21

#             *
#            / \
#           3   +
#              / \
#             5   2

class Tree:

	def __init__(self,value, children):
		self.value = value
		self.children = children

	def display(self, level=0):
		for i in range(level):
			print("   ", end="")
		print(self.value)
		if len(self.children) != 0:
			for child in self.children:
				child.display(level+1)

	def contains(self,value):
		if self.value == value:
			return True
		else:
			found = False
			for child in self.children:
				if not found:
					found = child.contains(value)
			return found


menu = Tree("Repas", [
		Tree("Entrées", [ Tree("Salade",[]), Tree("Pâté",[])  ]),
		Tree("Plats", [ Tree("Pizza",[]), Tree("Burger",[]), Tree("Tartiflette",[])  ]),
		Tree("Desserts", [ Tree("Tiramisu",[]), Tree("Baba au rhum",[])  ])
	])

menu.display()
print(menu.contains("Burger"))
print(menu.contains("Brocoli"))
