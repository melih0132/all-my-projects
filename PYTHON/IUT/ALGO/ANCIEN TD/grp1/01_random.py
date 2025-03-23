
from random import *
import time

t = []
max = 1500

before = time.time()

# Ne répond pas au problème : doublons
# for i in range(24):
# 	t.append(randrange(0,24))

# Version avec le "in"
# while len(t) < max:
# 	n = randrange(0,max)
# 	if not n in t:
# 		t.append(n)

# Version sans le "in"
# while len(t) < max:
# 	n = randrange(0,max)
# 	i = 0
# 	found = False
# 	while i < len(t) and not found:
# 		found = t[i] == n
# 		i += 1
# 	if not found:
# 		t.append(n)


available = []
for i in range(max):
	available.append(i)

for i in range(max):
	index = randrange(0,len(available))
	n = available.pop(index)
	t.append(n)




after = time.time()
print(after-before)
# print(t)
