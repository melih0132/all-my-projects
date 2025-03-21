

#-----------------------------------------------
# N premiers entier
# décroissant
def recIntDesc(n):
	print(n,end=" ")
	if n!=0:
		recIntDesc(n-1)

recIntDesc(7)

#-----------------------------------------------
# N premiers entier
# croissant
def recIntAsc(n, inc=0):
	print(inc, end=" ")
	if inc!=n:
		recIntAsc(n,inc+1)

recIntAsc(7)


#-----------------------------------------------
# Somme des premiers nombres
def recSum(n):
	if n==0:
		return 0
	else:
		return n+recSum(n-1)

print(recSum(7))

#-----------------------------------------------
def recConcat(t):
	if t == []:
		return ""
	else:
		return t[0] + recConcat(t[1:])

print(recConcat(["H","O","P", "!!!!"]))

#-----------------------------------------------
# Retourne un booléen qui dit si "v" est dans "t"
def recContains(t,v):
	if t == []:
		return False
	else:
		return t[0]==v or recContains(t[1:],v)
	

print(recContains(["burger","pizza","pâtes"], "pizza"))
print(recContains(["burger","pizza","pâtes"], "sushi"))

