
from random import *
import time


before = time.time()

max = 10000
t = []

# Version 1 : avec le "in" de Python
# Temps pour 10000 : environ 4s
# for i in range(max):
# 	x = randrange(1,max+1)
# 	while x in t:
# 		x = randrange(1,max+1)
# 	t.append(x)

# Version 2 : SANS le "in" de Python
# Temps pour 10000 : environ 80 secondes 
# while len(t) != max:
# 	x = randrange(1,max+1)
# 	i = 0
# 	found = False
# 	while i < len(t) and not found:
# 		found = t[i] == x
# 		i += 1
# 	if not found:
# 		t.append(x)

# Version 3 : Boucles imbriquées interdites !
# Temps pour 10000 : environ ...

available = []
for i in range(max):
	available.append(i)

for i in range(max):
	t.append(available.pop(randrange(0,len(available))))



after = time.time()
print(len(t))
# print(t)
print(after-before)
