import sys, pygame
pygame.init()
w,h = 1024, 768
screen = pygame.display.set_mode((w,h))
 
screen.fill((0,0,0))
color = (255,255,255)
 
#pygame.draw.aaline(screen, color, a, b)
 
#--------------------------------------------------------
 
def flake(n, a, b):
    ax, ay = a
    bx, by = b
    if n==0:
        pygame.draw.aaline(screen, color, a, b)
    else:
        c = (ax+(bx-ax)/3 , ay+(by-ay)/3)
        d = (ax+2*(bx-ax)/3 , ay+2*(by-ay)/3)
        e = ( (ax+bx)/2+(by-ay)/3 , (ay+by)/2-(bx-ax)/3)
        flake(n-1, a, c)
        flake(n-1, c, e)
        flake(n-1, e, d)
        flake(n-1, d, b)
 
flake(7, (100, 200), (900, 400))
 
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
 