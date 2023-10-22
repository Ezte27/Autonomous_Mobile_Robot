import pygame, random
from math import atan2, cos, pi, sin
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 25, 40)
WHITE = (255, 255, 255)

x1 = 50
y1 = 50
x2 = WIDTH
y2 = HEIGHT
angle = atan2(y2 - y1, x2 - x1) * 180 / pi
print(angle)
radius1 = 5
radius2 = 30

'''
line1x1 = x1 + angle // pi
line1y1 = y1 - radius2
line2x1 = x1 - angle // pi
line2y1 = y1 + radius2

line1x2 = x2 + angle // pi
line1y2 = y2 - radius2
line2x2 = x2 - angle // pi
line2y2 = y2 + radius2
'''

foundGoal = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if foundGoal:
        randsample = (random.randint(x1 - radius2, x2 + radius2), random.randint(y1 - radius2, y2 + radius2))
    else:
        randsample = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, RED, (x1, y1), radius1, 0)
    pygame.draw.circle(screen, RED, (x2, y2), radius1, 0)
    pygame.draw.circle(screen, BLACK, (x1, y1), radius2, 1)
    pygame.draw.circle(screen, BLACK, (x2, y2), radius2, 1)
    #pygame.draw.circle(screen, RED, (x2 + (radius2 / pi) , y2 - angle), radius1, 0)
    #pygame.draw.circle(screen, RED, (x2 - angle , y2 + (radius2 / pi)), radius1, 0)
    #screen.blit(surf1, rect1)
    #pygame.draw.line(screen, BLACK, (line1x1, line1y1), (line1x2, line1y2), 2)
    #pygame.draw.line(screen, BLACK, (line2x1, line2y1), (line2x2, line2y2), 2)
    pygame.draw.rect(screen, BLACK, ((x1 - radius2,y1- radius2), (abs((x2 - x1) + radius2 * 2), abs((y2 - y1) + radius2 * 2))), 1)
    pygame.draw.circle(screen, BLACK, randsample, radius1 + 5, 0)
    

    pygame.display.update()
    clock.tick(1)
pygame.quit()