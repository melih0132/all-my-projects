


class Tree:

	def __init__(self,value,children=[]):
		self.value = value
		self.children = children

	def indentstr(self, level=0):
		s = (level*"   ") + self.value +"\n"
		for node in self.children:
			s += node.indentstr(level+1)
		return s

	def __str__(self):
		return self.indentstr()

	def nbLeaves(self):
		if len(self.children) == 0:
			return 1
		else:
			n = 0
			for node in self.children:
				n += node.nbLeaves()
			return n

	def depth(self):
		if len(self.children) == 0:
			return 1
		else:
			max = 0
			for node in self.children:
				d = 1+node.depth()
				if d>max:
					max = d
			return max



menu =  Tree(
			"Menu",
			[
				Tree("Entrées",[
					Tree("Saucisson"),
					Tree("Salade")
				]),
				Tree("Plats", [
					Tree("Burger"),
					Tree("Pizza"),
					Tree("Rebloch'", [
						Tree("Croziflette"),
						Tree("Tartiflette")
					])
				]),
				Tree("Desserts", [
					Tree("Tiramisu"),
					Tree("Profiterolles")
				])
			])
print(menu)
print(menu.nbLeaves())
print(menu.depth())