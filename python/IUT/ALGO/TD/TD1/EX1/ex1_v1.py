from random import randrange

array = []
while len(array) < 24:
    value = randrange(1, 25)
    if value not in array:
        array.append(value)

print(array)