import pygame
import time
import sys
from RRT_Base import GREEN, RED, GREY, BLUE, WHITE, BLACK
from AutonomousMobileRobot.path_planning.rrt.misc.RRT_Star import RRT_STAR
from Differential_Drive.environment import Environment
from Differential_Drive.robot import Robot

# Variables
WIDTH = 800
HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
FPS = 10000
MAX_ITER = 1000000

ready = False

mapWindowName = 'RRT* PATH_PLANNING'
pygame.display.set_caption(mapWindowName)
clock = pygame.time.Clock()

rrt = RRT_STAR(DIMENSIONS, 40, 40, FPS, MAX_ITER, init_pygame=True)
rrt.run_rrt()
screen = rrt.screen

isPathFound = rrt.graph.goalFlag

start = rrt.start
goal = rrt.goal
obstacles = rrt.obstacles

dt = 0
lasttime = pygame.time.get_ticks()

if isPathFound:
    path = rrt.graph.getPathCoords()
    path.reverse()
    parent = []

else:
    print('No Path Found!')
    time.sleep(3)
    sys.exit()

# Differential Drive Robot Variables
controlPoints = path
environment = Environment(DIMENSIONS, screen)
environment.path = controlPoints
x_path, y_path = environment.B_spline()
robot_path = []
for x, y in zip(x_path, y_path):
    robot_path.append((x,y))
robot = Robot(controlPoints[0], 30, autonomous=True, path=robot_path)

def make_node():
    for i, node in enumerate(path):
        if i == 0:
            pygame.draw.circle(screen, GREEN, node, 7)
            parent.append(i)
        elif i == len(path) - 1:
            pygame.draw.circle(screen, RED, node, 12)
            parent.append(i)
        else:
            pygame.draw.circle(screen, GREY, node, 5)
            parent.append(i)

def draw_nodes():
    for i, node in enumerate(path):
        if i == 0:
            pygame.draw.circle(screen, GREEN, node, 7)
        elif i == len(path) - 1:
            pygame.draw.circle(screen, RED, node, 12)
        else:
            pygame.draw.circle(screen, GREY, node, 5)

def make_edge():
    for i in range(3):
        if i == 0:
            start = parent.pop(0)
        elif i == 1:
            goal = parent.pop(len(parent) - 1)
    parent.insert(0, start)
    parent.append(goal)
            
    for i, n in enumerate(path):
        if i == len(path) - 1:
            continue
        node1 = parent[i]
        node2 = parent[i + 1]
        x1, y1 = path[node1]
        x2, y2 = path[node2]
        pygame.draw.line(screen, BLUE, (x2, y2), (x1, y1), 1)

def draw_edges():
    for i, n in enumerate(path):
        if i == len(path) - 1:
            continue
        node1 = parent[i]
        node2 = parent[i + 1]
        x1, y1 = path[node1]
        x2, y2 = path[node2]
        pygame.draw.line(screen, BLUE, (x2, y2), (x1, y1), 1)

running = True

make_node()
make_edge()
FPS = 1000
while running:
    clock.tick(FPS)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            ready = True
    
    for obs in obstacles:
        pygame.draw.rect(screen, GREY, obs)

    draw_nodes()
    if not ready:
        draw_edges()
    if ready:
        robot.move_ai()

        for x, y in robot_path:
            pygame.draw.circle(screen, RED, (x, y), 2)
        
        robot.draw(screen)
        
        environment.create_trail((robot.x, robot.y)) # show the robot and the b_splined path which the robbot should follow.
    pygame.display.update()
    dt = (pygame.time.get_ticks() - lasttime)/1000 # secs
    lasttime = pygame.time.get_ticks()
    robot.dt = 0.189
pygame.quit()