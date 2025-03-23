
def mystery(x,y=0,z=0):
	if x<=0:
		return z
	elif x!=y:
		return mystery(x-1,y,z+x)
	else:
		return mystery(x,y,z)




print(mystery(10))
print(mystery(4))
print(mystery(0))
