import random, pygame, math
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (25, 25, 239)
GREEN = (20, 240, 28)
RED = (235, 30, 25)
BLACK = (0, 0, 0)
MAGENTA = (250, 20, 255)
TRANSPARENT = (0, 0, 0, 255)

class RRTMap:
    def __init__(self, mapDimensions, obsDimensions, obsNum, map=None):
        self.start = None
        self.goal = None
        self.mapDimensions = mapDimensions
        self.mapw, self.maph = self.mapDimensions

        # Window Settings
        self.mapWindowName = 'RRT PATH_PLANNING'
        pygame.display.set_caption(self.mapWindowName)
        self.map = map if map else pygame.display.set_mode((self.mapw, self.maph))
        self.map.fill(WHITE)
        self.nodeRad = 2
        self.nodeThickness = 2
        self.edgeThickness = 2
        
        self.obstacles = []
        self.obsDim = obsDimensions
        self.obsNum = obsNum

        self.isObsDrawn = False


    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, GREEN, self.start, self.nodeRad+5.0)
        pygame.draw.circle(self.map, RED, self.goal, self.nodeRad+10.0)
        if not self.isObsDrawn:
            self.drawObs(obstacles)

    def drawPath(self, path):
        for node in path:
            pygame.draw.circle(self.map, RED, node, self.nodeRad+3, 0)
    
    def makeObs(self):
        obs = []
        # start_rect = pygame.Rect(self.start[0], self.start[1], 14, 14)
        # goal_rect  = pygame.Rect(self.goal[0], self.goal[1], 24, 24)

        for i in range(0, self.obsNum):
            #startGoalCol = True
            # while startGoalCol:
            #     obsPos = self.makeRandomRect()
            #     rect = pygame.Rect(obsPos, (self.obsDim, self.obsDim))
            #     if rect.colliderect(start_rect) or rect.colliderect(goal_rect):
            #         startGoalCol = True
                
            #     else:
            #         startGoalCol = False
            obsPos = self.makeRandomRect()
            rect = pygame.Rect(obsPos, (self.obsDim, self.obsDim))
            obs.append(rect)
        self.obstacles = obs.copy()
        return obs
    
    def makeRandomRect(self):
        self.xObs = int(random.uniform(0, self.mapw-self.obsDim))
        self.yObs = int(random.uniform(0, self.maph-self.obsDim))

        return (self.xObs, self.yObs)

    def drawObs(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.map, GREY, obstacle)#pygame.draw.rect(self.map, random.choice([BLACK, GREY]), self.obstacle)
        self.isObsDrawn = True
    
    def make_start_and_goal(self):
        self.map.fill(WHITE)

        #self.makeObs()

        collide_start = False
        collide_goal = False

        isDrawingStart = True
        isDrawingGoal = False
        isDrawingObs = False

        start = None
        goal = None
        start_rect = None
        goal_rect = None
        obstacles = []

        ready = False
        running = True

        while running:
            self.map.fill(WHITE)
            self.drawObs()
            if start:
                pygame.draw.circle(self.map, GREEN, start, self.nodeRad+5.0)
            if goal:
                pygame.draw.circle(self.map, RED, goal, self.nodeRad+10.0)

        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and goal:
                        ready = True
                    elif event.key == pygame.K_1:
                        isDrawingStart = True
                        isDrawingGoal  = False
                        isDrawingObs   = False
                    elif event.key == pygame.K_2:
                        isDrawingStart = False
                        isDrawingGoal  = True
                        isDrawingObs   = False
                    elif event.key == pygame.K_3:
                        isDrawingStart = False
                        isDrawingGoal  = False
                        isDrawingObs   = True

                if not start or not goal:
                    ready = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if isDrawingStart:
                            start = pygame.mouse.get_pos()
                            start_rect = pygame.draw.circle(self.map, GREEN, start, self.nodeRad+5.0)
                            collide_start = False
                            for obstacle in obstacles:
                                if obstacle.colliderect(start_rect):
                                    collide_start = True
                                    start = None
                                    start_rect = None
                                    break
                        
                            if not collide_start:
                                pygame.draw.circle(self.map, GREEN, start, self.nodeRad+5.0)

                        elif isDrawingGoal:
                            goal = pygame.mouse.get_pos()
                            goal_rect = pygame.draw.circle(self.map, RED, goal, self.nodeRad + 10)
                            collide_goal = False
                            for obstacle in self.obstacles:
                                if obstacle.colliderect(goal_rect):
                                    collide_goal = True
                                    goal = None
                                    goal_rect = None
                                    break
                            
                            if not collide_goal:
                                pygame.draw.circle(self.map, RED, goal, self.nodeRad + 10)

                        elif isDrawingObs:
                            obsPos = pygame.mouse.get_pos()
                            obs_rect = pygame.Rect(obsPos, (self.obsDim, self.obsDim))
                            obs_rect.center = obsPos
                            collides = False
                            for point in [start_rect, goal_rect]:
                                if point:
                                    if point.colliderect(obs_rect):
                                        collides = True
                                        break
                            
                            if not collides:
                                obstacles.append(obs_rect)
                                pygame.draw.rect(self.map, GREY, obs_rect)
                    
                    elif event.button == 3:
                        mouse_pos = pygame.mouse.get_pos()
                        if start:
                            if start_rect.collidepoint(mouse_pos):
                                start = None
                                start_rect = None

                        if goal:
                            if goal_rect.collidepoint(mouse_pos):
                                goal = None
                                goal_rect = None

                        for obstacle in obstacles: 
                            if obstacle.collidepoint(mouse_pos):
                                obstacles.remove(obstacle)

                if ready:
                    running = False
                pygame.display.update()
                self.obstacles = obstacles
        self.start, self.goal = start, goal
        return start, goal, obstacles

class RRTGraph:
    def __init__(self, map, start, goal, mapDimensions, obstacles):
        (self.xStart, self.yStart) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.mapDimensions = mapDimensions
        self.mapw, self.maph = self.mapDimensions
        self.map = map

        self.X = []
        self.Y = []
        self.parent = []

        # Initialize the tree
        self.X.append(self.xStart)
        self.Y.append(self.yStart)
        self.parent.append(0)

        # Obstacles
        self.obstacles = obstacles

        # Path
        self.goalState = None
        self.path = []

        # RRT* Variables
        self.searchRadius = 55

    def add_node(self, n, x, y):
        self.X.insert(n, x)
        self.Y.insert(n, y)

    def remove_node(self, n):
        self.X.pop(n)
        self.Y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child, parent)

    def remove_edge(self, n):
        self.parent.pop(n)

    def make_edge_white(self, parent, child):
        pass

    def number_of_nodes(self):
        return len(self.X)

    def distance(self, n1, n2):
        (x1, y1) = (self.X[n1], self.Y[n1])
        (x2, y2) = (self.X[n2], self.Y[n2])
        px = (float(x1) - float(x2))**2
        py = (float(y1) - float(y2))**2
        return (px+py)**(0.5)

    def sample_environment(self):
        if self.goalFlag:
            try:
                costToGoal = self.cost(self.goalState)
                costToGoal = costToGoal // 2
            except:
                costToGoal = 0 #costToGoal // 4
            costToGoal = 0
            x = int(random.uniform(self.start[0] - costToGoal, self.goal[0] + costToGoal))
            y = int(random.uniform(self.start[1] - costToGoal, self.goal[1] + costToGoal))
        else:
            x = int(random.uniform(0, self.mapw))
            y = int(random.uniform(0, self.maph))
        return (x, y)

    def nearest(self, n):
        dmin = self.distance(0, n)
        nNear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nNear = i
        return nNear

    def isFree(self):
        n = self.number_of_nodes() - 1
        (x, y) = (self.X[n], self.Y[n])
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rect = obs.pop(0)
            if rect.collidepoint(x, y):
                self.remove_node(n)
                return False
        return True

    def doesEdgeCrossObstacles(self, x1, x2, y1, y2):
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rect = obs.pop(0)
            for i in range(200): # 200 point between the initial node and the node it is connecting to.
                u = i/200
                x=x1*u + x2*(1-u)
                y=y1*u + y2*(1-u)
                if rect.collidepoint(x, y):
                    return True
        return False

    def connect(self, n1, n2):
        (x1, y1) = (self.X[n1], self.Y[n1])
        (x2, y2) = (self.X[n2], self.Y[n2])

        xNearest = n1
        #costN2 = self.distance(xNearest, n2)#distance between nearest and new nodes
        cheapestNeighbor = 0
        bestNeighbor = 0
        cost_of_neighbor = 0
        if self.doesEdgeCrossObstacles(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        
        else:
            self.add_edge(n1, n2)
            cheapestNeighbor, neighbors = self.neighborsInRadius(n2)
            # Connects the New Node to the cheapest neighbor
            if not self.doesEdgeCrossObstacles(self.X[cheapestNeighbor], x2, self.Y[cheapestNeighbor], y2):
                self.remove_edge(n2)
                self.add_edge(cheapestNeighbor, n2)
         
            costN2 = self.cost(n2)
            for n in neighbors:
                cost_of_neighbor = self.cost(n)
                if costN2 + self.distance(n, n2) < cost_of_neighbor:
                    #cost_of_neighbor = costN2 + self.distance(n2, n)
                    if not self.doesEdgeCrossObstacles(self.X[n], self.X[n2], self.Y[n], self.Y[n2]):  
                        self.parent[n] = n2
         
            return True

    def step(self, nNear, nRand, dMax=35):
        distance = self.distance(nNear, nRand)
        if distance > dMax:
            u = dMax/distance
            (xNear, yNear) = (self.X[nNear], self.Y[nNear])
            (xRand, yRand) = (self.X[nRand], self.Y[nRand])
            (px, py) = (xRand - xNear, yRand - yNear)
            theta = math.atan2(py, px)
            (x, y) = (int(xNear + dMax * math.cos(theta)),
                      int(yNear + dMax * math.sin(theta)))
            self.remove_node(nRand)
            if abs(x-self.goal[0]) <= dMax and abs(y - self.goal[1]) <= dMax:
                self.add_node(nRand, self.goal[0], self.goal[1])
                self.goalState = nRand
                self.goalFlag = True
            else:
                self.add_node(nRand, x, y)

    def bias(self, nGoal):
        n = self.number_of_nodes()
        self.add_node(n, nGoal[0], nGoal[1])
        nNear = self.nearest(n)
        self.step(nNear, n)
        self.connect(nNear, n)
        return self.X, self.Y, self.parent

    def expand(self):
        n = self.number_of_nodes()
        x, y = self.sample_environment()
        self.add_node(n, x, y)
        if self.isFree():
            xNearest = self.nearest(n)
            self.step(xNearest, n)
            self.connect(xNearest, n)
        return self.X, self.Y, self.parent

    def path_to_goal(self):
        try:
            if self.goalFlag:
                self.path = []
                self.path.append(self.goalState)
                newPos = self.parent[self.goalState]
                while newPos != 0:
                    self.path.append(newPos)
                    newPos = self.parent[newPos]
                self.path.append(0)
            return self.goalFlag
        except:
            return False

    def getPathCoords(self):
        self.pathCoords = []
        self.path_to_goal()
        for node in self.path:
            x, y = (self.X[node], self.Y[node])
            self.pathCoords.append((x, y))
        return self.pathCoords
    

    # RRT* Functions

    def cost(self, n):
        startNode = 0
        parent = self.parent[n]
        cost = 0
        while n is not startNode:
            cost += self.distance(n, parent)
            n = parent
            if n is not startNode:
                parent = self.parent[n]
        return cost

    def neighborsInRadius(self, node):
        neighbors = []
        bestNeighbor = 0
        cheapestNeighbor = 0
        minCost = 1000
        x, y = (self.X[node], self.Y[node])
        circle = pygame.draw.circle(self.map, BLACK, (x, y), self.searchRadius, 1)
        for i in range(0, len(self.X)):
            if i == node:
                continue
            if circle.collidepoint((self.X[i], self.Y[i])):
                neighbors.append(i)
            else:
                pass
        for n in neighbors:
                nCost = self.cost(n)
                if nCost < minCost:
                    minCost = nCost
                    cheapestNeighbor = n

        return cheapestNeighbor, neighbors
        
        '''
        for n in neigbors:
            nCost = self.cost(n)
            Costs.append(nCost)
        return Costs
        '''

        # Differential Drive Robot

    def waypointsToPath(self):
        old_path = self.getPathCoords()
        path = []
        for i in range(0, len(self.path) - 1):
            if i >= len(self.path):
                break
            x1, y1 = old_path[i]
            x2, y2 = old_path[i + 1]
            for i in range(0, 5):
                u = i/5
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                path.append((x, y))
        return path