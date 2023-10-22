import sys
import pygame
from AutonomousMobileRobot.path_planning.rrt.config import *
from AutonomousMobileRobot.path_planning.rrt.rrt_base import RRTBase

class RRT(RRTBase):
    def __init__(self, X, Q, x_init, x_goal, max_samples, r, prc=0.01):
        """
        Template RRT planner
        :param X: Search Space
        :param Q: list of lengths of edges added to tree
        :param x_init: tuple, initial location
        :param x_goal: tuple, goal location
        :param max_samples: max number of samples to take
        :param r: resolution of points to sample along edge when checking for collisions
        :param prc: probability of checking whether there is a solution
        """
        super().__init__(X, Q, x_init, x_goal, max_samples, r, prc)

    def rrt_search(self, pygame_draw=False, obstacles=None):
        """
        Create and return a Rapidly-exploring Random Tree, keeps expanding until can connect to goal
        https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree
        :return: list representation of path, dict representing edges of tree in form E[child] = parent
        """
        self.add_vertex(0, self.x_init)
        self.add_edge(0, self.x_init, None)

        # Pygame setup

        if pygame_draw:
            pygame.init()
            screen = pygame.display.set_mode((screen_width, screen_height))
            clock = pygame.time.Clock()
            pygame.display.set_caption("RRT")
        

        while True:
            for q in self.Q:  # iterate over different edge lengths until solution found or time out
                for i in range(q[1]):  # iterate over number of edges of given length to add
                    x_new, x_nearest = self.new_and_near(0, q)

                    if x_new is None:
                        continue

                    # connect shortest valid edge
                    self.connect_to_point(0, x_nearest, x_new)

                    solution = self.check_solution()
                    if solution[0]:
                        if pygame_draw:
                            pygame.quit()
                        return solution[1]
                    
                    if pygame_draw:
                        self.draw_search(obstacles, screen, clock)
                        
    def draw_search(self, obstacles, screen, clock, solution=None, ellipse_angle=None, xc=None, yc=None, w=None, h=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                            
        screen.fill(WHITE)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Draw nodes and edges
        for i, tree in enumerate(self.trees):
            for start, end in tree.E.items():
                if end is not None:
                    pygame.draw.circle(screen, BLUE, start, node_rad)   # Node or vertex
                    pygame.draw.line(screen, GREY, start, end)          # Edge
                        
        # Draw start and goal
        pygame.draw.circle(screen, RED, self.x_init, node_rad * 2)
        pygame.draw.circle(screen, GREEN, self.x_goal, node_rad * 2)

        # Draw solution and ellipse
        if solution is not None:
            for node in solution[1:-1]: # Exclude the first and last nodes as they are the start and goal nodes.
                pygame.draw.circle(screen, YELLOW, node, node_rad)
            
            rect = pygame.Rect(xc - w/2, yc - h/2, w, h)
            surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            surface.fill(WHITE)
            surface.set_colorkey(WHITE)
            surface.set_alpha(0)
            pygame.draw.ellipse(surface, PURPLE, (0, 0, w, h), width=1)
            rotated_surface = pygame.transform.rotate(surface, ellipse_angle)
            screen.blit(rotated_surface, rect)


        pygame.display.update()
        clock.tick(FPS)