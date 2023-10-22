import pygame, time
import numpy as np
from AutonomousMobileRobot.path_planning.rrt.config import *
from AutonomousMobileRobot.path_planning.rrt.informed_rrt_star import IRRTStar
from AutonomousMobileRobot.path_planning.rrt.search_space.search_space import SearchSpace
from AutonomousMobileRobot.path_planning.rrt.utilities.obstacle_generation import generate_random_obstacles

def main(X, Q, x_init, x_goal, max_samples, max_iterations, r, prc, rewire_count, obstacles):
    """
    Function that runs the RRT algorithm on a given map and renders with pygame
    :param X: Search Space
    :param Q: list of lengths of edges added to tree
    :param x_init: tuple, initial location
    :param x_goal: tuple, goal location
    :param max_samples: max number of samples to take
    :param r: resolution of points to sample along edge when checking for collisions
    :param prc: probability of checking whether there is a solution
    """

    # Transform the obstacles from [[x1, y1, x2, y2], ...] to [[x1, y1, w, h], ...]
    for obstacle in obstacles:
        obstacle[2] -= obstacle[0]
        obstacle[3] -= obstacle[1]

    # Running the algorithm
    rrt = IRRTStar(X, Q, x_init, x_goal, max_samples, r, prc, rewire_count)
    print("Starting Informed RRT Star...")
    start_time = time.perf_counter()
    solution, angle, xc, yc, a, b  = rrt.irrt_star(max_iterations, pygame_draw=True, obstacles=obstacles)
    print("Finished Informed RRT Star in", round(time.perf_counter() - start_time, 6), "seconds")

    # Pygame setup
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Informed RRT Star 2D Example")

    clock = pygame.time.Clock()

    while True:
        rrt.draw_search(obstacles, screen, clock, solution, angle, xc, yc, a, b)
        

if __name__ == "__main__":

    # Dimensions of Search Space
    X_dimensions = np.array([(0, 800), (0, 800)])

    # Start and goal locations
    x_init = (50, 600)
    x_goal = (750, 200)

    # Obstacles
    n           = 50                # number of obstacles
    obstacles   = generate_random_obstacles(len(X_dimensions), X_dimensions, x_init, x_goal, n)
    
    Q           = np.array([(32, 16)])  # length of tree edges
    r           = 1                 # resolution of points on each edge when checking for collisions
    max_samples = 1024*4              # max number of samples to take before timing out
    max_iterations = 256*1         # max number of iterations to take after the ellipse has been created
    prc         = 0.01              # probability of checking for a solution after adding a node to the tree
    rewire_count = 64                # number of branches to rewire 

    # Create Search Space
    X = SearchSpace(X_dimensions, obstacles)

    main(X, Q, x_init, x_goal, max_samples, max_iterations, r, prc, rewire_count, obstacles)