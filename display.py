import pygame
import heapq
import maze as create
from pathfinding.adaptedA import adaptedDriver
from pathfinding.forwardA import AForwardDriver

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

screen_width, screen_height = 500,500
pygame.init()
sc = pygame.display.set_mode((screen_width, screen_height))
running = True
pygame.display.set_caption("A* Path Finding Algorithm")
clock = pygame.time.Clock()

cell_size = 50
cols, rows = screen_width//cell_size, screen_height//cell_size

grid = []

class grid_cell:
    def __init__(self, row, col, height, width) -> None:
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * height     
        self.color = GREY
        self.width = width  
        self.height = height
    
    def getPost(self):
      return self.row, self.col
    
    def isBlank(self):
        return self.color == WHITE
    
    def isPath(self):
        return self.color == GREEN
    
    def isWall(self):
        return self.color == RED
    
    def reset(self):
        self.color == WHITE

    def makeWall(self):
        self.color == RED

    def makePath(self):
        self.color == GREEN

    def makeVisit(self):
        self.color = BLUE
    
    def draw(self, win):
         pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))



def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = grid_cell(i, j, gap, gap)
			grid[i].append(spot)

	return grid

def draw(win, grid, rows):
     win.fill(WHITE)
     for row in grid:
        for spot in row:
            spot.draw(win)
            # pygame.display.flip()
     
     draw_grid(win, rows, screen_width)
     pygame.display.update()

def travelMaze(path, maze, limited_maze):
     # Execute the path from planning
    while loc != (len(maze)-2, len(maze[0])-2) and maze[loc[0]][loc[1]] != 'w':
        up = (loc[0]-1, loc[1])
        down = (loc[0]+1, loc[1])
        left = (loc[0], loc[1]-1)
        right = (loc[0], loc[1]+1)
        if limited_maze[up[0]][up[1]] == 'w':
            grid[up[0]][up[1]].makeWall()
        elif limited_maze[up[0]][up[1]] == 'p':
            grid[up[0]][up[1]].makePath()
        grid[up[0]][up[1]].draw(sc)
    

        if limited_maze[down[0]][down[1]] == 'w':
             grid[down[0]][down[1]].makeWall()
        elif limited_maze[down[0]][down[1]] == 'p':
            grid[down[0]][down[1]].makePath()
        grid[down[0]][down[1]].draw(sc)


        if limited_maze[left[0]][left[1]] == 'w':
             grid[left[0]][left[1]].makeWall()
        elif limited_maze[left[0]][left[1]] == 'p':
             grid[left[0]][left[1]].makePath()
        grid[left[0]][left[1]].draw(sc)


        if limited_maze[right[0]][right[1]] == 'w':
             grid[right[0]][right[1]].makeWall()
        elif limited_maze[right[0]][right[1]] == 'p':
             grid[right[0]][right[1]].makePath()
        grid[right[0]][right[1]].draw(sc)
            
        grid[loc[0]][loc[1]].makeVisit()
        grid[loc[0]][loc[1]].draw(sc)

        loc = path[loc]

def main(maze, command):
    grid = make_grid(15, 800)
    print("going to draw!")

    draw(sc, grid, 10)

    while running:
        if command == 'adapt':
            adaptedDriver(maze)
        elif command == 'forward':
            AForwardDriver(maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

