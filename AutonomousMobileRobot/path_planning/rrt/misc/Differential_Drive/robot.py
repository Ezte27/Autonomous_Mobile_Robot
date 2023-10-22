import pygame
import math
BLUE = (20, 20, 250)
class Robot:
    def __init__(self, start_pos, width, robotimg = None, autonomous = False, path = []):
        self.m2p = 3779.52 #1 meter = 2 pixels
        self.width = width
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.theta = 0
        self.vr = 0
        self.vl = 0
        self.a = self.width//2
        self.u = 30
        self.w = 0
        self.maxspeed_u = 6.469 * self.m2p
        self.minspeed_u = 2.996 * self.m2p
        self.minspeed = 120.02 * self.m2p
        self.maxspeed = 10.05 * self.m2p
        
        self.dt = 0

        self.autonomous = autonomous
        self.reachedGoal = False

        self.image = pygame.Surface((self.width + 20, self.width), pygame.SRCALPHA)
        self.image.fill(BLUE)
        # self.image = pygame.image.load(robotimg)
        # self.image.convert_alpha()
        self.rotated_image = self.image
        self.rect = self.rotated_image.get_rect(center = (start_pos))

        self.waypoint = 0
        self.path = path
    
    def draw(self, window):
        window.blit(self.rotated_image, self.rect)
    
    def move(self, keys):
        if keys[pygame.K_a]:
            self.vr += self.m2p * self.dt
        if keys[pygame.K_d]:
            self.vl += self.m2p * self.dt
        self.vr = self.minspeed if not keys[pygame.K_a] else self.vr 
        self.vl = self.minspeed if not keys[pygame.K_d] else self.vl

        self.vr = self.maxspeed if self.vr > self.maxspeed else self.vr
        self.vl = self.maxspeed if self.vl > self.maxspeed else self.vl

        self.x += ((self.vl + self.vr) / 2) * math.cos(self.theta) * 0.01
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.theta) * 0.01
        self.theta += (self.vr - self.vl)/self.width * 0.01
        self.rotated_image = pygame.transform.rotozoom(self.image, math.degrees(self.theta), 1)
        self.rect = self.rotated_image.get_rect(center = (self.x, self.y))

    def move_ai(self):
        if not self.reachedGoal:
            self.x += (self.u*math.cos(self.theta) - self.a*math.sin(self.theta)*self.w) * self.dt
            self.y += (self.u*math.sin(self.theta) + self.a*math.cos(self.theta)*self.w) * self.dt
            self.theta += self.w * self.dt

            self.rotated_image = pygame.transform.rotozoom(self.image, math.degrees(-self.theta), 1)
            self.rect = self.rotated_image.get_rect(center = (self.x, self.y))
            if self.path:
                self.follow_path()
            else:
                print('No path for the robot to follow.')
    
    def follow_path(self):
        if not self.reachedGoal:
            target = self.path[self.waypoint]
            delta_x = target[0] - self.x
            delta_y = target[1] - self.y
            self.u = (delta_x * math.cos(self.theta) + delta_y * math.sin(self.theta)) * self.dt
            self.w = ((-1 / self.a) * math.sin(self.theta) * delta_x + (1/self.a) * math.cos(self.theta) * delta_y) * self.dt
            if self.calculate_distance((self.x, self.y), target) <= 10:
                self.waypoint += 1
            if self.waypoint >= len(self.path):
                self.reachedGoal = True

    def calculate_distance(self, point1, point2):
        d = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        return d