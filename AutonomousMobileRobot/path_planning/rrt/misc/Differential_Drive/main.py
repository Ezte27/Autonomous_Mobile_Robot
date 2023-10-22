from environment import *
from robot import Robot
import pygame
pygame.init()
dt = 0
lasttime = pygame.time.get_ticks()

WIDTH = 800
HEIGHT = 600
dimensions = (WIDTH, HEIGHT)
FPS = 60

window = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()

running = True
controlPoints = [(771, 364), (716, 347), (671, 338), (642, 320), (609, 309), (576, 298), (543, 287), (513, 305), (479, 298), (428, 255), (401, 234), (395, 189), (372, 152), (317, 125), (287, 109), (235, 90), (227, 93), (196, 78), (163, 69), (128, 69), (77, 24), (43, 24), (12, 10)]
controlPoints.reverse()
environment = Environment(dimensions, window)
environment.path = controlPoints
path = environment.B_spline()
x_path, y_path = path
path = []
for x, y in zip(x_path, y_path):
    path.append((x,y))
robot = Robot(controlPoints[0], 30, autonomous=True, path=path)

while running:
    clock.tick(FPS)
    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
        if False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(window, RED, pos, 7, 0)
                controlPoints.append(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    environment.path = controlPoints
                    print([controlPoints])
                    path = environment.B_spline()
                    x_path, y_path = path
                    for x, y in zip(x_path, y_path):
                        pygame.draw.circle(window, RED, (x, y), 2)

    if robot.autonomous:
        robot.move_ai()
        for x, y in path:
            pygame.draw.circle(window, RED, (x, y), 2)
    else:
        keys = pygame.key.get_pressed()
        robot.move(keys)
    
    robot.draw(window)
    
    environment.create_trail((robot.x, robot.y))

    pygame.display.update()
    dt = 1/6#(pygame.time.get_ticks() - lasttime)/1000 # secs
    lasttime = pygame.time.get_ticks()
    robot.dt = dt