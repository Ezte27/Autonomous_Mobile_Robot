from AutonomousMobileRobot.path_planning.rrt.utilities.geometry import distance_between_points

def cost_to_go(a: tuple, b: tuple) -> float:
    """
    :param a: current location
    :param b: next location
    :return: estimated segment cost-to-go from a to b
    """
    return distance_between_points(a, b)

def path_cost(E, a, b):
    """
    Cost of the unique path from x_init to x
    :param E: edges, in the form of E[child] = parent
    :param a: initial location
    :param b: goal location
    :return: cost of the unique path from x_init to x
    """
    cost = 0
    while b != a:
        p = E[b]
        cost += cost_to_go(b, p)
        b = p
    return cost

def segment_cost(a, b):
    """
    Cost of the line between x_near and x_new
    :param a: start of line
    :param b: end of line
    :return: cost of the segment from a to b
    """
    return distance_between_points(a, b)