

# class Game:

# 	def __init__(self, name):
# 		self.name = name

# 	def __str__(self):
# 		return self.name

# tg = Game("Tiny Glade")
# print(tg)




class A:
	def m(self):
		return self.__class__

class B(A):
	pass

a = A()
# print(a.m())
b = B()
print(b.m())






