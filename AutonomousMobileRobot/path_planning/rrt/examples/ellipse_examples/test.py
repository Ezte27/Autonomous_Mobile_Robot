import pygame
import numpy as np

# Define the parameters of the ellipse
a = 600  # Major axis length
b = 300  # Minor axis length

# Number of points for the ellipse
num_points = 100  # You can adjust this based on the desired resolution

# Calculate the angle increment
theta = np.linspace(0, 2 * np.pi, num_points)

# Calculate x and y coordinates for the points on the ellipse
x = a * np.cos(theta)
y = b * np.sin(theta)

# Pygame Setup
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 
pygame.display.set_caption("Ellipse")
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

points = list(zip(x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    screen.fill(WHITE)

    # Draw the ellipse
    for point in points:
        pygame.draw.circle(screen, BLACK, (point[0] + SCREEN_WIDTH/2, point[1] + SCREEN_HEIGHT/2), 2)
    
    pygame.display.update()
    clock.tick(FPS)