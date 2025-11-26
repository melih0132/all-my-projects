def recIntDesc(n):
    if n > 0:
        print(n)
        recIntDesc(n - 1)

def recIntAsc(n, start=1):
    if start <= n:
        print(start)
        recIntAsc(n, start + 1)

def recSum(n):
    return n + recSum(n - 1) if n > 0 else 0

def recConcat(array, i=0):
    return array[i] + recConcat(array, i + 1) if i < len(array) else ""

def recPos(array, value, i=0):
    return True if i < len(array) and (array[i] == value or recPos(array, value, i + 1)) else False
