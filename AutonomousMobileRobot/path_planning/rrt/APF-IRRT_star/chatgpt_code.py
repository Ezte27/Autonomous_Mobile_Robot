import random
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0  # Cost to reach this node

class APF_IRRTStar:
    def __init__(self, start, goal, obstacles, max_iterations, step_size, goal_radius):
        self.start = Node(*start)
        self.goal = Node(*goal)
        self.obstacles = obstacles
        self.max_iterations = max_iterations
        self.step_size = step_size
        self.goal_radius = goal_radius
        self.nodes = [self.start]

    def distance(self, node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def steer(self, nearest_node, random_node):
        # Calculate the direction vector
        dx = random_node.x - nearest_node.x
        dy = random_node.y - nearest_node.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        dx /= dist
        dy /= dist

        # Generate a new node in the direction of the random node
        new_x = nearest_node.x + self.step_size * dx
        new_y = nearest_node.y + self.step_size * dy

        return Node(new_x, new_y)

    def is_collision_free(self, new_node):
        for obstacle in self.obstacles:
            if self.distance(new_node, obstacle) < 1.0:
                return False
        return True

    def find_nearest_node(self, random_node):
        min_dist = float('inf')
        nearest_node = None

        for node in self.nodes:
            dist = self.distance(random_node, node)
            if dist < min_dist:
                min_dist = dist
                nearest_node = node

        return nearest_node

    def rewire_tree(self, new_node):
        for node in self.nodes:
            if node != new_node.parent and self.distance(new_node, node) < self.step_size:
                if self.is_collision_free(node):
                    new_cost = new_node.cost + self.distance(new_node, node)
                    if new_cost < node.cost:
                        node.parent = new_node
                        node.cost = new_cost

    def generate_path(self, end_node):
        path = []
        current_node = end_node
        while current_node:
            path.append((current_node.x, current_node.y))
            current_node = current_node.parent
        return path[::-1]

    def apf(self):
        k_att = 1.0
        k_rep = 100.0
        max_repulsive_force = 10.0
        d_goal = self.distance(self.start, self.goal)

        while len(self.nodes) < self.max_iterations:
            random_node = Node(random.uniform(0, 10), random.uniform(0, 10))
            nearest_node = self.find_nearest_node(random_node)
            new_node = self.steer(nearest_node, random_node)

            if self.is_collision_free(new_node):
                self.nodes.append(new_node)
                new_node.parent = nearest_node
                new_node.cost = nearest_node.cost + self.distance(new_node, nearest_node)

                if self.distance(new_node, self.goal) < self.goal_radius:
                    self.rewire_tree(new_node)
                    if new_node.cost + self.distance(new_node, self.goal) < d_goal:
                        path = self.generate_path(new_node)
                        return path

        return None

if __name__ == "__main__":
    start_node = (1, 1)
    goal_node = (9, 9)
    obstacle_nodes = [Node(3, 3), Node(4, 4), Node(6, 6)]
    max_iterations = 1000
    step_size = 0.5
    goal_radius = 1

    planner = APF_IRRTStar(start_node, goal_node, obstacle_nodes, max_iterations, step_size, goal_radius)
    path = planner.apf()

    if path:
        print("Path found:")
        for node in path:
            print(node)
    else:
        print("Path not found")