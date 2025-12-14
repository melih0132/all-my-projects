# Fonction 1 : Affiche les N premiers entiers en ordre décroissant
def recIntDesc(n):
    if n <= 0:
        return
    print(n)
    recIntDesc(n - 1)

print("f1 :")
recIntDesc(7)


# Fonction 2 : Affiche les N premiers entiers en ordre croissant
def recIntAsc(n, current=1):
    if current > n:
        return
    print(current)
    recIntAsc(n, current + 1)

print("f2 :")
recIntAsc(7)


# Fonction 3 : Calcule la somme des N premiers entiers
def recSum(n):
    if n == 0:
        return 0
    else:
        return n + recSum(n - 1)

print("f3 :")
print(recSum(10))


# Fonction 4 : Concatène les éléments d'un tableau de chaînes de caractères
def recConcat(strings, index=0):
    if index == len(strings):
        return ""
    else:
        return strings[index] + recConcat(strings, index + 1)

print("f4 :")
print(recConcat(["ça ", "marche."]))


# Fonction 5 : Vérifie si une valeur est contenue dans un tableau
def recPos(arr, value, index=0):
    if index == len(arr):
        return False
    if arr[index] == value:
        return True
    return recPos(arr, value, index + 1)

print("f5 :")
print(recPos([1, 2, 3, 4, 5], 5))