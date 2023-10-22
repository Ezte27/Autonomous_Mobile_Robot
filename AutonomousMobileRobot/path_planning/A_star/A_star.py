import pygame
import pathlib, os
import json, random, time
from queue import PriorityQueue


WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
 

CWD = pathlib.Path(__file__).parent # or os.getcwd()
MAZE_PATH = os.path.join(CWD, "Mazes.json")
MAPED = True
if MAPED:
    with open(MAZE_PATH, 'r') as f:
        data = json.load(f)
    MAPS = data["A*_Maps"]
    ROWS = 40
else:
    ROWS = 40

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_close(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE
    
    def make_start(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE
    
    def make_white(self):
        self.color = WHITE
    
    def make_player(self):
        self.color = GREY

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #hw(n) = ε ha(n), ε > 1
    cost = abs(x1 - x2) + abs(y1 - y2)
    return cost

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        #draw()

def algorithm(draw, grid, start, end):
    global player
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    won = False

    while not open_set.empty() and not won:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             playerx, playery = player.get_pos()
        #             spotUp = grid[playerx][playery - 1]
        #             if spotUp == end:
        #                 time.sleep(2.5)
        #                 won = True
        #                 break
        #             if spotUp.is_open() and playery - 1 >= 0:
        #                 player.make_white()
        #                 player = spotUp
        #                 player.make_player()

        #         if event.key == pygame.K_DOWN:
        #             playerx, playery = player.get_pos()
        #             if playery + 1 < ROWS :
        #                 spotDown = grid[playerx][playery + 1]
        #                 if spotDown == end:
        #                     time.sleep(2.5)
        #                     won = True
        #                     break
        #                 if spotDown.is_open():
        #                     player.make_white()
        #                     player = spotDown
        #                     player.make_player()
                    
        #         if event.key == pygame.K_RIGHT:
        #             playerx, playery = player.get_pos()
        #             if playerx + 1 < ROWS:
        #                 spotRight = grid[playerx + 1][playery]
        #                 if spotRight == end:
        #                     time.sleep(2.5)
        #                     won = True
        #                     break
        #                 if spotRight.is_open():
        #                     player.make_white()
        #                     player = spotRight
        #                     player.make_player()

        #         if event.key == pygame.K_LEFT:
        #             playerx, playery = player.get_pos()
        #             if playerx - 1 >= 0:
        #                 spotLeft = grid[playerx - 1][playery]
        #                 if spotLeft == end:
        #                     time.sleep(2.5)
        #                     won = True
        #                     break
        #                 if spotLeft.is_open():
        #                     player.make_white()
        #                     player = spotLeft
        #                     player.make_player()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        #draw()

        if current != start:
            current.make_close()
    
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
        
    return grid

def draw_grid(win, rows, width):
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*GAP), (width, i*GAP))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*GAP, 0), (j*GAP, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def make_maze(map, width):
    grid = []
    rows = ROWS
    gap = width // rows
    icount = 0
    jcount = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(icount, jcount, gap, rows)
            for k, row in enumerate(map):
                for l, col in enumerate(row):
                    if l == '.':
                        print('a')
                        spot.make_white()
                    elif l == 'O':
                        print('a')
                        spot.make_barrier()
                    elif l == 'S':
                        print('a')
                        spot.make_start()
                    elif l == 'E':
                        print('a')
                        spot.make_end()
            grid[icount].append(spot)
            jcount += 1
        icount += 1
    return grid

def main(win, width): 
    global player
    grid = make_grid(ROWS, width)
    start = None
    end = None
    player = None
    run = True
    started = False
    tik = 0.0
    tok = 0.0

    while run:
        if tik > 0.0:
            tok = time.perf_counter()
            print(int(tok - tik))

        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started == False:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_mouse_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end and spot != player:
                        start = spot
                        start.make_start()

                    elif not end and spot != start and spot != player:
                        end = spot
                        end.make_end()
                    
                    elif not player and spot != start and spot != end:
                        player = spot
                        player.make_player()
                        tik = time.perf_counter()
                        
                    elif spot != start and spot != end and spot != player:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_mouse_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                    elif spot == player:
                        player = None

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP and player:
                        playerx, playery = player.get_pos()
                        spotUp = grid[playerx][playery - 1]
                        if spotUp.is_open() and playery - 1 >= 0:
                            player.make_white()
                            player = spotUp
                            player.make_player()

                    if event.key == pygame.K_DOWN and player:
                        playerx, playery = player.get_pos()
                        if playery + 1 < ROWS :
                            spotDown = grid[playerx][playery + 1]
                            if spotDown.is_open():
                                player.make_white()
                                player = spotDown
                                player.make_player()
                    
                    if event.key == pygame.K_RIGHT and player:
                        playerx, playery = player.get_pos()
                        if playerx + 1 < ROWS:
                            spotRight = grid[playerx + 1][playery]
                            if spotRight.is_open():
                                player.make_white()
                                player = spotRight
                                player.make_player()

                    if event.key == pygame.K_LEFT and player:
                        playerx, playery = player.get_pos()
                        if playerx - 1 >= 0:
                            spotLeft = grid[playerx - 1][playery]
                            if spotLeft.is_open():
                                player.make_white()
                                player = spotLeft
                                player.make_player()

                    if event.key == pygame.K_SPACE and not started or tok - tik >= 30.0:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        
                        start_time = time.perf_counter()
                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        print(f'Time taken: {time.perf_counter() - start_time}')
                        started = True
                        tik = 0.0
                        tok = 0.0
                    if event.key == pygame.K_m and MAPED: # press M to make maze
                        MAP = MAPS[random.randint(0, len(MAPS) - 1)]["map"]
                        
                        for i, row in enumerate(MAP):
                            for j, col in enumerate(row):
                                spot = grid[j][i]
                                if col == '.':
                                    spot.make_white()
                                elif col == 'O':
                                    spot.make_barrier()
                                elif col == 'S':
                                    start = spot
                                    spot.make_start()
                                elif col == 'E':
                                    end = spot
                                    spot.make_end()
                        
                    if event.key == pygame.K_s and not started and not MAPED: # Press S to save 
                        with open(MAZE_PATH, 'r') as f:
                            data = json.load(f)
                        maze = []
                        lineperrow = ''
                        temp = {
                            "id": 0,
                            "map": maze
                        }
                        for i in range(ROWS):
                            lineperrow = ''
                            for j in range(ROWS):
                                spot = grid[i][j]
                                if spot.is_barrier():
                                    lineperrow += 'O'
                                elif spot.is_open():
                                    lineperrow += '.'
                                elif spot.is_start():
                                    lineperrow += 'S'
                                elif spot.is_end():
                                    lineperrow += 'E'
                            maze.append(lineperrow)
                        data["A*_Maps"].append(temp)
                        with open(MAZE_PATH, 'w') as f:
                            json.dump(data, f, indent=4)
                        print('SAVED!')
            else:
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_r:
                        grid = make_grid(ROWS, width)
                        started = False
                        start = None
                        end = None
                        player = None
                        tok = 0.0
                        tik = 0.0
                        for row in grid:
                            for spot in row:
                                spot.make_white()
                        

    pygame.quit()

main(WIN, WIDTH)