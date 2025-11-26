
import sys, pygame
pygame.init()
w,h = 1024, 768
screen = pygame.display.set_mode((w,h))

screen.fill((0,0,0))
color = (255,200,100)


# def triangle(n, p1, p2, p3):
# 	if n == 1:
# 		pygame.draw.aaline(screen, color, p1, p2)
# 		pygame.draw.aaline(screen, color, p2, p3)
# 		pygame.draw.aaline(screen, color, p3, p1)
# 	else:
# 		p1x,p1y = p1
# 		p2x,p2y = p2
# 		p3x,p3y = p3
# 		p4 = ((p1x+p2x)/2, (p1y+p2y)/2 )
# 		p5 = ((p1x+p3x)/2, (p1y+p3y)/2 )
# 		p6 = ((p2x+p3x)/2, (p2y+p3y)/2 )
# 		triangle( n-1, p1, p4, p5)
# 		triangle( n-1, p2, p4, p6)
# 		triangle( n-1, p3, p5, p6)


# triangle( 10,  (500,100) , (100,700) , (900,700) )




def flake(n, p1, p2):
	if n==1:
		pygame.draw.aaline(screen, color, p1, p2)
	else:
		p1x,p1y = p1
		p2x,p2y = p2
		vx,vy = (p2x-p1x, p2y-p1y)
		p3 = p1x+vx/3 , p1y+vy/3
		p5 = p1x+2*vx/3 , p1y+2*vy/3
		p4 = p1x+vx/2-vy/3,p1y+vy/2+vx/3
		flake(n-1,  p1, p3)
		flake(n-1,  p3, p4)
		flake(n-1,  p4, p5)
		flake(n-1,  p5, p2)



flake(7, (100,300), (800, 400))




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

















