
import sys, pygame
pygame.init()
w,h = 1024, 768
screen = pygame.display.set_mode((w,h))

screen.fill((0,0,0))
color = (255,200,100)
#--------------------------------------------------------



def triangle(n, a,b,c):
	ax,ay = a
	bx,by = b
	cx,cy = c
	if n==1:
		pygame.draw.aaline(screen, color, a, b)
		pygame.draw.aaline(screen, color, b, c)
		pygame.draw.aaline(screen, color, c, a)
	else:
		triangle(n-1, a, ((bx+ax)/2, ((by+ay)/2)), ((cx+ax)/2, ((cy+ay)/2)))
		triangle(n-1, b, ((bx+ax)/2, ((by+ay)/2)), ((cx+bx)/2, ((cy+by)/2)))
		triangle(n-1, c, ((bx+cx)/2, ((by+cy)/2)), ((cx+ax)/2, ((cy+ay)/2)))


triangle(7, (100,100), (800,400), (200, 600))












#--------------------------------------------------------

play = True
clock = pygame.time.Clock()

while play:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			play = False
		if event.type == pygame.KEYUP:
			print(event.key, event.unicode, event.scancode)
			if event.key == pygame.K_ESCAPE:
				play = False


	clock.tick(60)
	pygame.display.flip()



