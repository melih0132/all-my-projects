



def integers(n):
	if n==1:
		print(n) # Il ne reste qu'un seul M&M's -> condition d'arrêt
	else:
		print(n) # manger M&M's
		integers(n-1) # Filer le paquet au voisin

#integers(7)



def concatenate(t1,t2):
	if t1 ==[]:
		return t2
	else:
		return [ t1[0],  concatenate(t1[1:], t2) ]


print(concatenate( [42, 73], [ "hop", "pizza" ] ))




