from operator import itemgetter

import pygame, sys, math, random, copy

from AutonomousMobileRobot.path_planning.rrt.config import *
from AutonomousMobileRobot.path_planning.rrt.utilities.geometry import distance_between_points, check_node_in_ellipse
from AutonomousMobileRobot.path_planning.rrt.heuristics import path_cost
from AutonomousMobileRobot.path_planning.rrt.rrt_star import RRTStar

class IRRTStar(RRTStar):
    def __init__(self, X, Q, x_init, x_goal, max_samples, r, prc=0.01, rewire_count=None):
        """
        IRRT* Search
        :param X: Search Space
        :param Q: list of lengths of edges added to tree
        :param x_init: tuple, initial location
        :param x_goal: tuple, goal location
        :param max_samples: max number of samples to take
        :param r: resolution of points to sample along edge when checking for collisions
        :param prc: probability of checking whether there is a solution
        :param rewire_count: number of nearby vertices to rewire
        """
        super().__init__(X, Q, x_init, x_goal, max_samples, r, prc, rewire_count)

        # Ellipse parameters
        self.focus1, self.focus2 = x_init, x_goal
        self.x_ellipse, self.y_ellipse = self._get_midpoint(x_init, x_goal) # center of ellipse
        self.angle = math.atan2((self.focus2[1] - self.focus1[1]), (self.focus2[0] - self.focus1[0])) # Angle in radians
        self.a = 0
        self.b = 0
        self.cmin = distance_between_points(self.focus1, self.focus2) # minimum distance between focus points

        # Other parameters
        self.past_solution = None
        self.best_cbest = float('inf')

    def update_ellipse(self, cbest=None):
        self.a = self.best_cbest / 2 if cbest is None else cbest / 2
        self.b = math.sqrt(self.best_cbest**2 - self.cmin**2) / 2 if cbest is None else math.sqrt(cbest**2 - self.cmin**2) / 2

    def check_delta_solution(self, solution:list) -> bool: # Check for change in solution
        """
        Parameters
        ----------
        solution : list
            The path that has been found by the RRT algorithm

        Returns
        -------
        bool
            True if the solution has changed, False otherwise.
        """
        if self.past_solution != solution:
            self.past_solution = solution
            return True
        return False

    def check_better_solution(self, tree):
        """
        This method checks if there is a better solution than the current solution by comparing the current solution's cbest with the new solution. The new solution is searched in this method.
        """
       
        solution = self.reconstruct_path(tree, self.x_init, self.x_goal)
        if solution != self.past_solution:
            print("New solution found!")
        return solution
    
    def rewire_node_to_goal(self, tree):
        """
        Rewire branches near goal to shorten solution if possible
        Only rewires vertices according to rewire count
        :param tree: int, tree to rewire
        :return:
        """
        # get nearby vertices and cost-to-come
        L_near = self.get_nearby_vertices(0, self.x_init, self.x_goal)

        # check nearby vertices for total cost and connect shortest valid edge
        self.connect_shortest_valid(0, self.x_goal, L_near)

    def check_new_cbest(self, tree):
        new_cbest = path_cost(self.trees[tree].E, self.focus1, self.focus2)
        print(f'previous cbest = {self.best_cbest}')
        print(f'new cbest = {new_cbest}')
        print(f'cost decreased by {self.best_cbest - new_cbest}')
        if (new_cbest < self.best_cbest):
            self.best_cbest = new_cbest

    @staticmethod
    def _get_midpoint(a, b):
        """
        Get midpoint of two points
        :param a: tuple, first point
        :param b: tuple, second point
        :return: tuple, midpoint of points
        """
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    def irrt_star(self, max_iterations : int, pygame_draw : bool = False, obstacles : list = None):
        """
        Based on algorithm found in: Informed RRT*: Optimal Sampling-based Path Planning Focused via Direct Sampling of an Admissible Ellipsoidal Heuristic
        https://arxiv.org/pdf/1404.2334.pdf
        :return: set of Vertices; Edges in form: vertex: [neighbor_1, neighbor_2, ...]
        """
        self.add_vertex(0, self.x_init)
        self.add_edge(0, self.x_init, None)

        # Pygame setup

        if pygame_draw:
            pygame.init()
            screen = pygame.display.set_mode((screen_width, screen_height))
            clock = pygame.time.Clock()
            pygame.display.set_caption("Informed RRT Star")

        iteration = 0

        # Run RRT*
        while True: # Run until solution is found
            for q in self.Q:  # iterate over different edge lengths
                for i in range(q[1]):  # iterate over number of edges of given length to add
                    x_new, x_nearest = self.new_and_near(0, q)
                    if x_new is None:
                        continue

                    # get nearby vertices and cost-to-come
                    L_near = self.get_nearby_vertices(0, self.x_init, x_new)

                    # check nearby vertices for total cost and connect shortest valid edge
                    self.connect_shortest_valid(0, x_new, L_near)

                    if x_new in self.trees[0].E:
                        # rewire tree
                        self.rewire(0, x_new, L_near)

                    solution = self.check_solution() 
                    if solution[0]:
                        # When solution is found, an ellipse is created
                        print("Solution Found!")
                        print("Creating ellipse...") 
                        cbest = path_cost(self.trees[0].E, self.focus1, self.focus2)
                        self.update_ellipse(cbest)
                        solution = solution[1]          # Changing the solution variable from [bool, list of nodes] to just list of nodes
                        self.past_solution = solution   # Updating the past solution variable

                        # Run IRRT*
                        while iteration < max_iterations:
                            for q2 in self.Q:  # iterate over different edge lengths
                                for j in range(q2[1]):  # iterate over number of edges of given length to add
                                    x_new, _ = self.new_and_near(0, q)
                                    if x_new is None:
                                        continue

                                    # Check if the node created is outside the ellipse
                                    if not check_node_in_ellipse(x_new, self.x_ellipse, self.y_ellipse, self.a, self.b, self.angle):
                                        continue

                                    # get nearby vertices and cost-to-come
                                    L_near = self.get_nearby_vertices(0, self.x_init, x_new)

                                    # check nearby vertices for total cost and connect shortest valid edge
                                    self.connect_shortest_valid(0, x_new, L_near)

                                    if x_new in self.trees[0].E:
                                        # rewire tree
                                        self.rewire(0, x_new, L_near)
                                    
                                    self.rewire_node_to_goal(0)

                                    # Update solution
                                    solution = self.check_better_solution(0)

                                    # If solution changed, update the ellipse
                                    if self.check_delta_solution(solution): 
                                        
                                        print(f'NEW solution = {solution}')

                                        self.check_new_cbest(0)

                                        # Update ellipse parameters
                                        self.update_ellipse()
                                    
                                    if pygame_draw:
                                        self.draw_search(obstacles, screen, clock, solution, self.angle, self.x_ellipse, self.y_ellipse, self.a, self.b)
                            iteration += 1
                        return solution, self.angle, self.x_ellipse, self.y_ellipse, self.a, self.b                      
                    
                    if pygame_draw:
                        self.draw_search(obstacles, screen, clock)