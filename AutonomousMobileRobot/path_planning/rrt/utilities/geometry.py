from itertools import tee
import numpy as np
import math

def distance_between_points(a, b):
    """
    Calculates the Euclidean distance between two points
    :param a: first point
    :param b: second point
    :return: Euclidean distance between a and b
    """
    return np.linalg.norm(np.array(b) - np.array(a))

def pairwise(iterable):
    """
    Returns an iterator over all pairs of elements in iterable
    :param iterable: iterable to iterate over
    :return: s -> (s0, s1), (s1, s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def es_points_along_line(start, end, r):
    """
    Equally spaced points along a line defined by start, end, and r
    :param start: start point
    :param end: end point
    :param r: maximum distance between points
    :return: list of equally spaced points along the line, separated by distance r
    """
    d = distance_between_points(start, end)
    n_points = int(np.ceil(d / r))
    if n_points > 1:
        step = d / (n_points - 1)
        for i in range(n_points):
            next_point = steer(start, end, step * i)
            yield next_point

def steer(start, end, d):
    """
    Return a point in the direction of end, that is distance away from start
    :param start: start point
    :param end: end point
    :param d: distance away from start
    :return: point in the direction of end, that is distance away from start
    """
    start, end = np.array(start), np.array(end)
    v = end - start
    u = v / (np.sqrt(np.sum(v ** 2)))
    steered_point = start + u * d
    return tuple(steered_point)

def check_node_in_ellipse(node, x_ellipse, y_ellipse, a, b, angle):
    """
    Check if node is within ellipse
    :param node: node to check
    :param x_ellipse: ellipse x coordinate
    :param y_ellipse: ellipse y coordinate
    :param a: ellipse a parameter
    :param b: ellipse b parameter
    :param angle: ellipse angle in radians
    :return: boolean, True if node is within ellipse, False otherwise
    """
    return (((((math.cos(angle)*(node[0] - x_ellipse) + math.sin(angle)*(node[1] - y_ellipse))**2)/(a**2)) + (((math.sin(angle)*(node[0] - x_ellipse) - math.cos(angle)*(node[1] - y_ellipse))**2)/(b**2))) <= 1)