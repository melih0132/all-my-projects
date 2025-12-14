



def hanoi(origin, temp, destination, n):
	if n == 1:
		print(origin + " -> " + destination)
	else:
		hanoi(origin, destination, temp, n-1)
		print(origin + " -> " + destination)
		hanoi(temp, origin, destination, n-1)

hanoi("A","B","C", 7)
