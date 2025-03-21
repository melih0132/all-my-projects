

# Cas plus simple que les arbres

class LinkedList:

	def __init__(self,value,next):
		self.value = value
		self.next = next

	def display(self):
		print(self.value)
		if self.next:
			self.next.display()

	def count(self):
		if self.next == None:
			return 1
		else:
			return 1 + self.next.count()

	def add(self, value):
		if self.next == None:
			self.next = LinkedList(value, None)
		else:
			self.next.add(value)

	def elem(self,n):
		if n == 0:
			return self.value
		else:
			return self.next.elem(n-1)


list = LinkedList("Tanguy", 
		LinkedList("Robin", 
		LinkedList("Berkan",
		LinkedList("Victor", 
		LinkedList("Nathan", 
		LinkedList("Eya", 
		None))))))

# print(list.value)
# print(list.next.value)
# print(list.next.next.value)
# print(list.next.next.next.value)

list.display()
print(list.count())
list.add("Florian")
list.display()
print(list.elem(3))