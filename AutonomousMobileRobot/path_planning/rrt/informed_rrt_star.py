from operator import itemgetter

import pygame, sys, math, random, copy

from AutonomousMobileRobot.path_planning.rrt.config import *
from AutonomousMobileRobot.path_planning.rrt.utilities.geometry import distance_between_points, check_node_in_ellipse
from AutonomousMobileRobot.path_planning.rrt.heuristics import path_cost, segment_cost
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

    def update_ellipse(self, cbest):
        self.a = cbest / 2
        self.b = math.sqrt(cbest**2 - self.cmin**2) / 2

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
        # check for new solution
        x_nearest = self.get_nearest(tree, self.x_goal)
        if self.prc and random.random() < self.prc:
            # if self.X.collision_free(x_nearest, self.x_goal, self.r):  # check if obstacle-free
            if self.check_solution_cost(tree, x_nearest):
                print("New solution found!!!")
                self.trees[tree].E[self.x_goal] = x_nearest
                solution = self.reconstruct_path(tree, self.x_init, self.x_goal)
                self.best_cbest = path_cost(self.trees[tree].E, self.focus1, self.focus2)
                return solution
        return self.past_solution
    
    def check_solution_cost(self, tree, x_nearest):
        """
        Creates a duplicate tree where you reconstruct the path and then check if cost of new solution is less than current solution cost.
        :param tree: int, tree being checked
        :return: bool, True if cost is less than current solution cost, False otherwise.
        """
        self.trees.append(copy.deepcopy(self.trees[tree]))
        self.trees[tree+1].E[self.x_goal] = x_nearest
        new_solution = self.reconstruct_path(tree+1, self.x_init, self.x_goal)
        new_cbest = path_cost(self.trees[tree+1].E, self.focus1, self.focus2)
        del self.trees[tree+1]
        return (new_cbest < self.best_cbest) # The less the cost the better

    def check_new_cbest(self, tree):
        new_cbest = path_cost(self.trees[tree].E, self.focus1, self.focus2)
        if (new_cbest < self.best_cbest):
            self.best_cbest = new_cbest

    def rewire_goal(self, tree, x_goal):
        """
        Rewire branches near goal to shorten solution if possible
        Only rewires vertices according to rewire count
        :param tree: int, tree to rewire
        :param x_goal: tuple, the goal location
        :param L_near: list of nearby vertices used to rewire
        :return:
        """
        # get nearby vertices and cost-to-come
        L_near = self.get_nearby_vertices(0, self.x_init, x_goal)

        for c_near, x_near in L_near:
            curr_cost = path_cost(self.trees[tree].E, self.x_init, x_near)
            tent_cost = path_cost(self.trees[tree].E, self.x_init, x_goal) + segment_cost(x_goal, x_near)
            if tent_cost < curr_cost and self.X.collision_free(x_near, x_goal, self.r):
                self.trees[tree].E[x_near] = x_goal

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
                        solution = solution[1]
                        print(f'NEW solution FORMAT = {solution}')
                        self.past_solution = solution

                        # Run IRRT*
                        while iteration < max_iterations:
                            for q in self.Q:  # iterate over different edge lengths
                                for i in range(q[1]):  # iterate over number of edges of given length to add
                                    x_new, x_nearest = self.new_and_near(0, q)
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
                                    
                                    self.rewire_goal(0, self.x_goal)

                                    self.check_new_cbest(0) #solution = self.check_better_solution(0)
                                    self.update_ellipse(cbest)

                                    # Update solution
                                    solution = self.check_better_solution(0)

                                    # If solution changed, update the ellipse
                                    if self.check_delta_solution(solution): 
                                        print(f'NEW solution = {solution}')
                                    
                                    if pygame_draw:
                                        self.draw_search(obstacles, screen, clock, solution, self.angle, self.x_ellipse, self.y_ellipse, self.a, self.b)
                            iteration += 1
                        return solution                      
                    
                    if pygame_draw:
                        self.draw_search(obstacles, screen, clock)