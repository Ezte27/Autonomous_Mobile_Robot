import numpy as np
screen_width = 800
screen_height = 800

FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY  = (85, 85, 85)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

node_rad = 5

# Define the parameters of the rotated ellipse

point_rad = 3

# Number of points for the ellipse
num_points = 100  # You can adjust this based on the desired resolution

# Calculate the angle increment
theta = np.linspace(0, 2 * np.pi, num_points)