import pygame
import math

def draw_koch_curve(screen, p1, p2, depth):
    """ Dessine récursivement le flocon de Koch. """
    if depth == 0:
        pygame.draw.line(screen, (255, 255, 255), p1, p2)
    else:
        x1, y1 = p1
        x2, y2 = p2

        dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
        pA = (x1 + dx, y1 + dy)
        pB = (x1 + 2 * dx, y1 + 2 * dy)

        mx, my = (pA[0] + pB[0]) / 2, (pA[1] + pB[1]) / 2
        height = math.sqrt(dx**2 + dy**2) * math.sqrt(3) / 2
        pC = (mx - dy * math.sqrt(3) / 2, my + dx * math.sqrt(3) / 2)

        draw_koch_curve(screen, p1, pA, depth - 1)
        draw_koch_curve(screen, pA, pC, depth - 1)
        draw_koch_curve(screen, pC, pB, depth - 1)
        draw_koch_curve(screen, pB, p2, depth - 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill((0, 0, 0))

    draw_koch_curve(screen, (100, 400), (700, 400), 4)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
