import pygame
import math
import numpy as np
from scipy import interpolate

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
RED = (250, 20, 20)
GREEN = (20, 250, 20)
BLUE = (20, 20, 250)
YELLOW = (250, 250, 40)

class Environment:
    def __init__(self, dimensions, window):
        # colors
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.trail_set = []

        self.window = window
        self.path = [] # path found by the rrt* algorithm
    
    def create_trail(self, pos):
        for i in range(0, len(self.trail_set) - 1):
            pygame.draw.line(self.window,
                             BLACK,
                             (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__()>6000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)
    
    def B_spline(self):
        x = []
        y = []

        for point in self.path:
            x.append(point[0])
            y.append(point[1])

        tck, _ = interpolate.splprep([x, y])
        u = np.linspace(0, 1, num=100)
        smooth_path = interpolate.splev(u, tck)

        return smooth_path
