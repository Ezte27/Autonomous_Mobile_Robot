import pygame, time
from RRT_Base import *

run = False

WIDTH = 800
HEIGHT = 600
FPS = 10
MAX_ITER = 2000

dimension = (WIDTH, HEIGHT)

class RRT_STAR:
    def __init__(self, dimension, obsDim, obsNum, fps, max_iter, init_pygame = False):
        self.FPS                              = fps
        self.MAX_ITER                         = max_iter
        self.dimension                        = dimension

        pygame.init() if init_pygame else None
        self.screen                           = pygame.display.set_mode(self.dimension)

        self.rrt_map                          = RRTMap(dimension, obsDim, obsNum, self.screen)
        self.start, self.goal, self.obstacles = self.rrt_map.make_start_and_goal()
        self.rrt_map.drawMap(self.obstacles)

        self.graph                            = RRTGraph(self.screen, self.start, self.goal, dimension, self.obstacles)

        self.Clock                            = pygame.time.Clock()

    def run_rrt(self):
        costRepeated = 0
        oldCost = 0
        iteration = 0
        running = True

        while running:
            self.Clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
            if iteration % 10 == 0:
                X, Y, Parent = self.graph.bias(self.goal)
                pygame.draw.circle(self.screen, GREY, (X[-1], Y[-1]), self.rrt_map.nodeRad + 2, 0)
                pygame.draw.line(self.screen, BLUE, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), self.rrt_map.edgeThickness)
            else:
                X, Y, Parent = self.graph.expand()
                pygame.draw.circle(self.screen, GREY, (X[-1], Y[-1]), self.rrt_map.nodeRad + 2, 0)
                pygame.draw.line(self.screen, BLUE, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), self.rrt_map.edgeThickness)

            # if iteration > 1000 and not self.graph.goalFlag:
            #     running = False

            if self.graph.path_to_goal() and iteration > self.MAX_ITER:
                running = False
            if self.graph.path_to_goal():
                self.rrt_map.drawPath(self.graph.getPathCoords())
                if oldCost == 0:
                    oldCost = self.graph.cost(self.graph.goalState)
                else:
                    if oldCost == self.graph.cost(self.graph.goalState):
                        costRepeated += 1
                    else:
                        oldCost = self.graph.cost(self.graph.goalState)
                        costRepeated = 0
                            
            if costRepeated == self.MAX_ITER // 8.5:
                running = False

            iteration += 1
            pygame.display.update()
        if self.graph.goalFlag:
            # self.screen.fill(WHITE)
            # self.rrt_map.drawPath(self.graph.getPathCoords())
            pygame.display.update()
            waypoints = self.graph.waypointsToPath()
 
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

if __name__ == '__main__' and run == True:
    rrt_star = RRT_STAR(dimension, 40, 40, FPS, MAX_ITER, init_pygame=True)
    rrt_star.run_rrt()
    screen = rrt_star.screen
    path   = rrt_star.graph.getPathCoords()
    path.reverse()
    parent = []
    obstacles = rrt_star.obstacles
    make_node()
    make_edge()
    running = True
    while running: # while loop to keep the window from closing
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for obs in obstacles:
            pygame.draw.rect(screen, GREY, obs)
        draw_nodes()
        draw_edges()
        pygame.display.update()
    pygame.quit()