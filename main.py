import pygame
import sys

pygame.init()

size = width, height = 800, 600
screen_bg = 50, 50, 50
BLUE = (91, 151, 251)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

x, y = 400, 300
vx, vy = 0, 0

friction_coefficient = 0.005

while True:
    constant = clock.tick(30) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        vy -= 10
    if keys[pygame.K_s]:
        vy += 10
    if keys[pygame.K_a]:
        vx -= 10
    if keys[pygame.K_d]:
        vx += 10

    vx -= friction_coefficient * vx
    vy -= friction_coefficient * vy

    x += vx * constant
    y += vy * constant

    if x >= 760 or x < 40:
        vx *= -1

    if y >= 560 or y < 40:
        vy *= -1



    color_r = max(0, min(255, 255 - abs(vx)))
    color_g = max(0, min(255, abs(vy)))

    screen.fill(screen_bg)
    pygame.draw.line(screen, BLUE, (0, 0), (int(x), int(y)), width=2)
    pygame.draw.line(screen, BLUE, (800, 0), (int(x), int(y)), width=2)
    pygame.draw.circle(screen, (color_r, color_g, 0), (int(x), int(y)), 40)

    pygame.display.flip()
