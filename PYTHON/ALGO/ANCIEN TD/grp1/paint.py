import PIL
from PIL import Image
import numpy as np

# pour pouvoir bourriner sur la récursivité
import sys
sys.setrecursionlimit(40000)
print(sys.getrecursionlimit())

# chargement de l'image sous forme de tableau
image = np.asarray(Image.open("lily.jpg"), dtype='int32')

# modification de l'image
h = len(image)
w = len(image[0])

def samePixel(p1, p2):
	return p1[0] == p2[0] and p1[1] == p2[1] and p1[2] == p2[2]

# def paint(image, point, color):
# 	global count
# 	count += 1
# 	x,y = point
# 	if samePixel(image[y][x], [255,255,255]):
# 		image[y][x] = color
# 		if y-1 >=0:
# 			paint(image, (x,y-1), color)
# 		if x+1 < w:
# 			paint(image, (x+1,y), color)
# 		if y+1 < h:
# 			paint(image, (x,y+1), color)
# 		if x-1 >= 0:
# 			paint(image, (x-1,y), color)


def paint(image, point, color):
	todo = [ point ]

	while len(todo) > 0:
		x,y = todo.pop(0)
		if samePixel(image[y][x], [255,255,255]):
			image[y][x] = color
			# if y-1 >=0:
			todo.append( (x,y-1) )
			# if y+1 < h:
			todo.append( (x,y+1) )
			# if x-1 >= 0:
			todo.append( (x-1,y) )
			# if x+1 < w:
			todo.append( (x+1,y) )



paint(image, (20,80), [100,255,100])
paint(image, (20,10), [100,100,255])

# enregistrement sous un nouveau nom
im = PIL.Image.fromarray(np.uint8(image))
im.save("lily_paint.jpg")