import numpy as np
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Define the parameters of the rotated ellipse
a = 300  # Major axis length
b = 200  # Minor axis length
angle = np.deg2rad(30)  # Rotation angle in radians
xcenter = SCREEN_WIDTH / 2    # X-coordinate of the center
ycenter = SCREEN_HEIGHT / 2   # Y-coordinate of the center

# Number of points for the ellipse
num_points = 1000  # You can adjust this based on the desired resolution

# Calculate the angle increment
theta = np.linspace(0, 2 * np.pi, num_points)

# Calculate x and y coordinates for the points on the rotated ellipse
x = xcenter + a * np.cos(theta) * np.cos(angle) - b * np.sin(theta) * np.sin(angle)
y = ycenter + a * np.cos(theta) * np.sin(angle) + b * np.sin(theta) * np.cos(angle)

# Pygame Setup
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 
pygame.display.set_caption("Ellipse")
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

points = list(zip(x, y))

while True:
    # Calculate x and y coordinates for the points on the rotated ellipse
    x = xcenter + a * np.cos(theta) * np.cos(angle) - b * np.sin(theta) * np.sin(angle)
    y = ycenter + a * np.cos(theta) * np.sin(angle) + b * np.sin(theta) * np.cos(angle)
    points = list(zip(x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    screen.fill(WHITE)

    # Draw the ellipse
    for point in points:
        pygame.draw.circle(screen, BLACK, (point[0], point[1]), 2)

    pygame.display.update()
    clock.tick(FPS)
    
    # Increment the angle
    angle += 0.01
