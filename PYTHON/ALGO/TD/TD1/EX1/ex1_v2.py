from random import randrange
import time

max = 10

before = time.time()
array = []
while len(array) < 24:
    value = randrange(1, 25)
    found = False
    for element in array:
        if element == value:
            found = True
            break
    if not found:
        array.append(value)

after = time.time()

""" before = time.time()
array = []
while len(array) < max:
    value = randrange(1, max - 1)
    found = False
    for element in array:
        if element == value:
            found = True
            break
    if not found:
        array.append(value)

after = time.time() """

""" array = []

before = time.time()

while len(array) < max:
    x = randrange(1, max - 1)
    found = False
    i = 0
    while i < len(array):
        if array[i] == x:
            found = True
            break
        i += 1
    if not found:
        array.append(x)

after = time.time() """

print(array)
print(after - before)