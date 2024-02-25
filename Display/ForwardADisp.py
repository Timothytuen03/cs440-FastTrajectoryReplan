import heapq
import mazes.maze as create
import pygame

heuristic = [[0 for _ in range(101)] for _ in range(101)]

num_rows = 101

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

screen_width, screen_height = 808,808
pygame.init()
sc = pygame.display.set_mode((screen_width, screen_height))
running = True
pygame.display.set_caption("A* Path Finding Algorithm")
clock = pygame.time.Clock()

# cols, rows = screen_width//cell_size, screen_height//cell_size
cols, rows = num_rows, num_rows
cell_size = screen_height//num_rows

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
    
    def isVisit(self):
        return self.color == BLUE
    
    def reset(self):
        self.color = WHITE

    def makeWall(self):
        self.color = RED

    def makePath(self):
        self.color = GREEN

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



def make_grid():
	grid = []
	# gap = width // rows
	for i in range(num_rows):
		grid.append([])
		for j in range(num_rows):
			spot = grid_cell(i, j, cell_size, cell_size)
            # spot = grid_cell(i, j, cell_size, cell_size)
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

def travelMaze(loc, path, maze, limited_maze):
     # Execute the path from planning
    print("traveling")
    while loc != (len(maze)-2, len(maze[0])-2) and maze[loc[0]][loc[1]] != 'w':
        up = (loc[0]-1, loc[1])
        down = (loc[0]+1, loc[1])
        left = (loc[0], loc[1]-1)
        right = (loc[0], loc[1]+1)

        # print(grid[up[0]][up[1]].isVisit())

        if not grid[up[0]][up[1]].isVisit():
            if maze[up[0]][up[1]] == 'w':
                grid[up[0]][up[1]].makeWall()
            # elif maze[up[0]][up[1]] == 'p':
            #     grid[up[0]][up[1]].makePath()
        grid[up[0]][up[1]].draw(sc)
    
        if not grid[down[0]][down[1]].isVisit():
            if maze[down[0]][down[1]] == 'w':
                grid[down[0]][down[1]].makeWall()
            # elif maze[down[0]][down[1]] == 'p':
            #     grid[down[0]][down[1]].makePath()
        grid[down[0]][down[1]].draw(sc)

        if not grid[left[0]][left[1]].isVisit():
            if maze[left[0]][left[1]] == 'w':
                grid[left[0]][left[1]].makeWall()
            # elif maze[left[0]][left[1]] == 'p':
            #     grid[left[0]][left[1]].makePath()
        grid[left[0]][left[1]].draw(sc)

        if not grid[right[0]][right[1]].isVisit():
            if maze[right[0]][right[1]] == 'w':
                grid[right[0]][right[1]].makeWall()
            # elif maze[right[0]][right[1]] == 'p':
            #     grid[right[0]][right[1]].makePath()
        grid[right[0]][right[1]].draw(sc)
            
        grid[loc[0]][loc[1]].makeVisit()
        grid[loc[0]][loc[1]].draw(sc)

        loc = path[loc]
        pygame.display.update()
        pygame.time.wait(200)
    if loc == (len(maze)-2, len(maze[0])-2):
        grid[loc[0]][loc[1]].makeVisit()
        grid[loc[0]][loc[1]].draw(sc)
        pygame.display.flip()


# START OF FORWARD A*

class PriorityQueue(object):
    def __init__(self) -> None:
        self.heap = []
        # self._index = 0 # For identical priorities

    def __str__(self) -> str:
        # return ' '.join(tuple(self.heap))
        return ' '.join(map(str, self.heap))
    
    def empty(self):
        return len(self.heap) == 0
    
    def add(self, element, g, priority):
        heapq.heappush(self.heap, (priority, g, element))
        # self._index += 1

    def remove(self):
        return heapq.heappop(self.heap)[-1]


def reversePath(path, end_cell, start_cell):
    corr_path = {}
    while end_cell != start_cell:
        next_loc = path[end_cell]
        corr_path[next_loc] = end_cell
        end_cell = next_loc

    return corr_path

def BasicA(maze, start, obstacles):
    # print(heuristic)
    # Eval Function: f(n) = g(n) + h(n)
    # f(n) - Estimated cost of cheapest solution through n
    # g(n) - path cost from start node to node n
    # h(n) - estimated cost of cheapest path from n to the goal (Manhattan distance). Curr Grid --> [100,100] 
    frontier = PriorityQueue()
    running_cost = {}
    f_scores = {}
    prev_loc = {}
    close_list = []

    frontier.add(start, 0, 0)
    running_cost[start] = 0
    prev_loc[start] = None

    while not frontier.empty():
        curr_loc = frontier.remove()
        # print(curr_loc)
        # print("frontier", frontier)
        close_list.append(curr_loc)

        up = (curr_loc[0]-1, curr_loc[1])
        down = (curr_loc[0]+1, curr_loc[1])
        left = (curr_loc[0], curr_loc[1]-1)
        right = (curr_loc[0], curr_loc[1]+1)
        
        # If reach goal, break
        if curr_loc == (len(maze)-2,len(maze[0])-2):
            # print("f scores: ", f_scores)
            return prev_loc, close_list, curr_loc

        # obstacles[curr_loc[0]][curr_loc[1]] = 'p'

        # Check four directions
        # Only add to frontier if not in closed list (hasn't been visited) and not a known wall
        g = running_cost[curr_loc]+1
        # Top
        if curr_loc[0] > 1 and (up not in close_list) and obstacles[up[0]][up[1]] != 'w':
            h = heuristic[up[0]][up[1]]
            f = g+h

            if (up not in f_scores) or g < running_cost[up]:
                frontier.add(up, g, f)
                f_scores[up] = f
                running_cost[up] = g
                prev_loc[up] = curr_loc

        # Bottom
        if curr_loc[0] < len(maze)-2 and (down not in close_list) and obstacles[curr_loc[0]+1][curr_loc[1]] != 'w':
            h = heuristic[down[0]][down[1]]
            f = g+h
            if (down not in f_scores) or g < running_cost[down]:
                running_cost[down] = g
                f_scores[down] = f
                frontier.add(down, g, f)
                prev_loc[down] = curr_loc
        # Left
        if curr_loc[1] > 1 and (left not in close_list) and obstacles[curr_loc[0]][curr_loc[1]-1] != 'w':
            h = heuristic[left[0]][left[1]]
            f = g+h

            if (left not in f_scores) or g < running_cost[left]:
                frontier.add(left, g, f)
                f_scores[left] = f
                running_cost[left] = g
                prev_loc[left] = curr_loc
        # Right
        if curr_loc[1] < len(maze[0])-2 and (right not in close_list) and obstacles[curr_loc[0]][curr_loc[1]+1] != 'w':
            h = heuristic[right[0]][right[1]]
            f = g+h

            if (right not in f_scores) or g < running_cost[right]:
                frontier.add(right, g, f)
                f_scores[right] = f
                running_cost[right] = g
                prev_loc[right] = curr_loc

    return prev_loc, close_list, curr_loc

def executeAForward(path, limited_maze, maze, loc):
    # Execute the path from planning
    prev = None
    # print("Executing plan")
    # print(loc)
    while loc != (len(maze)-2, len(maze[0])-2) and maze[loc[0]][loc[1]] != 'w':
        up = (loc[0]-1, loc[1])
        down = (loc[0]+1, loc[1])
        left = (loc[0], loc[1]-1)
        right = (loc[0], loc[1]+1)
        prev = loc
        limited_maze[up[0]][up[1]] = maze[up[0]][up[1]]
        limited_maze[down[0]][down[1]] = maze[down[0]][down[1]]
        limited_maze[left[0]][left[1]] = maze[left[0]][left[1]]
        limited_maze[right[0]][right[1]] = maze[right[0]][right[1]]
        limited_maze[loc[0]][loc[1]] = 'p'

        loc = path[loc]
        # print(loc)

    if loc == (len(maze)-2, len(maze[0])-2):
        return loc, limited_maze
    else:
        return prev, limited_maze

def AForwardDriver(maze):
    numExpanded = 0
    h = len(maze)
    w = len(maze[0])
    explored_maze = [['?' for _ in range(w)] for _ in range(h)]
    for i in range(h):
        for j in range(w):
            heuristic[i][j] = abs((len(maze)-2) - i) + abs(len(maze[0])-2 - j)


    loc = (1,1)
    while loc != (len(maze)-2, len(maze[0])-2):
        rev_path, close, curr_loc = BasicA(maze, loc, explored_maze)
        numExpanded = numExpanded + len(close)
        if curr_loc != (len(maze)-2, len(maze[0])-2):
            print("Impossible Maze!") 
            break

        path = reversePath(rev_path, (len(maze)-2, len(maze[0])-2), loc)
        # print("The Plan: ", path)
        new_loc, explored_maze = executeAForward(path, explored_maze, maze, loc)
        print("travel maze!")
        travelMaze(loc, path, maze, explored_maze)
        loc = new_loc
        
    print("A forward Maze:")
    create.printMaze(explored_maze, h, w)

    return numExpanded



if __name__ == "__main__":
    h = num_rows
    w = num_rows

    maze = create.main(h, w)
    # display.main(maze, command)
    grid = make_grid()
    print("going to draw!")

    draw(sc, grid, num_rows)
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print("key down")
                if event.key == pygame.K_RETURN:
                    print("hit space")
                    AForwardDriver(maze)