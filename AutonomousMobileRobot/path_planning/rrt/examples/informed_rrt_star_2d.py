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
    solution = rrt.irrt_star(max_iterations, pygame_draw=True, obstacles=obstacles)
    print("Finished Informed RRT Star in", round(time.perf_counter() - start_time, 6), "seconds")

    # Pygame setup
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Informed RRT Star 2D Example")

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Draw nodes and edges
        for i, tree in enumerate(rrt.trees):
            for start, end in tree.E.items():
                if end is not None:
                    pygame.draw.circle(screen, BLUE, start, node_rad)   # Node or vertex
                    pygame.draw.line(screen, GREY, start, end)          # Edge
        
        # Draw start and goal
        pygame.draw.circle(screen, RED, x_init, node_rad * 2)
        pygame.draw.circle(screen, GREEN, x_goal, node_rad * 2)

        # Draw solution
        if solution is not None:
            for node in solution[1:-1]: # Exclude the first and last nodes as they are the start and goal nodes.
                pygame.draw.circle(screen, YELLOW, node, node_rad)

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
        

if __name__ == "__main__":

    # Dimensions of Search Space
    X_dimensions = np.array([(0, 800), (0, 800)])

    # Start and goal locations
    x_init = (50, 400)
    x_goal = (750, 400)

    # Obstacles
    n           = 50                # number of obstacles
    obstacles   = generate_random_obstacles(len(X_dimensions), X_dimensions, x_init, x_goal, n)
    
    Q           = np.array([(32, 16)])  # length of tree edges
    r           = 1                 # resolution of points on each edge when checking for collisions
    max_samples = 1024*4              # max number of samples to take before timing out
    max_iterations = 200         # max number of iterations to take after the ellipse has been created
    prc         = 0.01              # probability of checking for a solution after adding a node to the tree# probability of checking for a connection to the goal after adding a node to the tree
    rewire_count = 5                # number of branches to rewire 

    # Create Search Space
    X = SearchSpace(X_dimensions, obstacles)

    main(X, Q, x_init, x_goal, max_samples, max_iterations, r, prc, rewire_count, obstacles)