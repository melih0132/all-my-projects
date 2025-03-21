from PIL import Image
import numpy as np

tt = np.asarray(Image.open("worm.jpg"))
t = tt.copy()

h = len(t)
w = len(t[0])

R = 0
G = 1
B = 2

# t : lignes de pixels y / x / rgb
#print(t[42][73][R])

padding = 60

for y,row in enumerate(t):
	for x,pixel in enumerate(row):

		if x < padding or y < padding or \
		   x > w-padding-1 or y > h-padding-1:

			pixel[R] = pixel[R]
			pixel[G] = 127
			pixel[B] = 0

		else:

			avg = (int(pixel[R])+int(pixel[G])+int(pixel[B]))//3
			pixel[R] = avg
			pixel[G] = avg
			pixel[B] = avg





im = Image.fromarray(t)
im.save("worm-modif.jpg")
