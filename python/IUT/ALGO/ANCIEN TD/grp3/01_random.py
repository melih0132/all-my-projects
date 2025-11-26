
from random import *
import time


MAX = 1500
t = []

before = time.time()


# VERSION 1 : EZ
# while len(t) < MAX:
# 	n = randrange(0,MAX)
# 	count += 1
# 	if not n in t:
# 		t.append(n)

# VERSION 2 : Sans le IN
# while len(t) < MAX:
# 	n = randint(0,MAX)
# 	i = 0
# 	found = False
# 	while not found and i < len(t):
# 		found = t[i] == n
# 		i += 1
# 	if not found:
# 		t.append(n)

# VERSION 3 : Pas de boucles imbriquées

numbers = []
for i in range(0,MAX):
	numbers.append(i)

for i in range(0,MAX):
	index = randint(0,len(numbers)-1)
	n = numbers.pop(index)
	t.append(n)

after = time.time()
print(after-before)

