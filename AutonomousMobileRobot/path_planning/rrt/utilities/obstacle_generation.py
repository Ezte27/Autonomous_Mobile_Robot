import random, uuid
from colorama import Fore
import numpy as np
from rtree import index


def generate_random_obstacles(dimensions, dimension_lengths, start, end, n):
    """
    Generates n random obstacles without disrupting world connectivity.
    It also respects start and end points so that they don't lie inside of an obstacle.
    """
    # Note: Current implementation only supports hyperrectangles.
    i = 0
    obstacles = []
    p = index.Property()
    p.dimension = dimensions
    X_obs = index.Index(interleaved=True, properties=p)
    while i < n:
        center = np.empty(len(dimension_lengths), np.float64)
        scollision = True
        fcollision = True
        edge_lengths = []
        for j in range(dimensions):
            # None of the sides of a hyperrectangle can be higher than 0.1 of the total span
            # in that particular X.dimensions
            max_edge_length = (dimension_lengths[j][1] - dimension_lengths[j][0]) / 10.0
            # None of the sides of a hyperrectangle can be higher than 0.01 of the total span
            # in that particular X.dimensions
            min_edge_length = (dimension_lengths[j][1] - dimension_lengths[j][0]) / 100.0
            edge_length = random.uniform(min_edge_length, max_edge_length)
            center[j] = random.uniform(dimension_lengths[j][0] + edge_length,
                                       dimension_lengths[j][1] - edge_length)
            edge_lengths.append(edge_length)

            if abs(start[j] - center[j]) > edge_length:
                scollision = False
            if abs(end[j] - center[j]) > edge_length:
                fcollision = False

        # Check if any part of the obstacle is inside of another obstacle.
        min_corner = np.empty(dimensions, np.float64)
        max_corner = np.empty(dimensions, np.float64)
        for j in range(dimensions):
            min_corner[j] = center[j] - edge_lengths[j]
            max_corner[j] = center[j] + edge_lengths[j]
        obstacle = np.append(min_corner, max_corner)
        # Check newly generated obstacle intersects any former ones. Also respect start and end points
        if len(list(X_obs.intersection(obstacle))) > 0 or scollision or fcollision:
            continue
        
        obstacles.append(obstacle)

        # Add the obstacle with the numerical ID
        X_obs.add(uuid.uuid4().int, tuple(obstacle), tuple(obstacle))

        i += 1

    return obstacles

def obstacle_generator(obstacles):
    """
    Add obstacles to r-tree
    :param obstacles: list of obstacles
    """
    for obstacle in obstacles:
        yield (uuid.uuid4().int, obstacle, obstacle)