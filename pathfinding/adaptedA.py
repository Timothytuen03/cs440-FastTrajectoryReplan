import heapq
import maze as create
heuristic = [[0 for _ in range(10)] for _ in range(10)]

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

def AdaptedA(maze, start, obstacles):
    
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
        # Update Heuristics of Expanded!
        def updateH():
            # print("updating heuristics")
            # max_key = curr_loc
            # max_value = f_scores[curr_loc]

            # for f in f_scores.items():
            #     print(f)
            #     key = f[0]
            #     value = f[1]
            #     # print(key)
            #     # print(value)
            #     if f_scores[key] < max_value:
            #         max_key = key
            #         max_value = value
            #     if f_scores[key] == max_value:
            #         if running_cost[key] > running_cost[max_key]:
            #             max_key = key
            #             max_value = value
        
            # print("close list: ", close_list)
            # for cell in close_list:
                # print("old h value ", cell, heuristic[cell[0]][cell[1]])
                # print("new h value ", cell, max_value - running_cost[cell])
            #     heuristic[cell[0]][cell[1]] = max_value - running_cost[cell]
            # print("Goal g: ", running_cost[(len(maze)-2, len(maze[0])-2)])
            for cell in close_list:
                # print(cell, running_cost[cell])
                # print("old h value ", cell, heuristic[cell[0]][cell[1]])
                old_h = heuristic[cell[0]][cell[1]]
                heuristic[cell[0]][cell[1]] = running_cost[(len(maze)-2, len(maze[0])-2)] - running_cost[cell]
                # print("diff h value ", cell,  heuristic[cell[0]][cell[1]] - old_h)
            # print("Heuristics: ", heuristic)
            

        curr_loc = frontier.remove()
        close_list.append(curr_loc)

        up = (curr_loc[0]-1, curr_loc[1])
        down = (curr_loc[0]+1, curr_loc[1])
        left = (curr_loc[0], curr_loc[1]-1)
        right = (curr_loc[0], curr_loc[1]+1)
        
        # If reach goal, break
        if curr_loc == (len(maze)-2,len(maze[0])-2):
            updateH()
            return prev_loc, close_list, curr_loc

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
                frontier.add(down, g, f)
                f_scores[down] = f
                running_cost[down] = g
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


def executeAdapted(path, limited_maze, maze, loc):
    # Execute the path from planning
    prev = None
    # print("Executing plan")
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

    if loc == (len(maze)-2, len(maze[0])-2):
        return loc, limited_maze
    else:
        return prev, limited_maze


def adaptedDriver(maze):
    numExpanded = 0
    h = len(maze)
    w = len(maze[0])
    explored_maze = [['?' for _ in range(w)] for _ in range(h)]
    for i in range(h):
        for j in range(w):
            heuristic[i][j] = abs((len(maze)-2) - i) + abs(len(maze[0])-2 - j)


    loc = (1,1)
    while loc != (len(maze)-2, len(maze[0])-2):
        rev_path, close, curr_loc = AdaptedA(maze, loc, explored_maze)
        numExpanded = numExpanded + len(close)
        if curr_loc != (len(maze)-2, len(maze[0])-2):
            print("Impossible Maze!") 
            break

        path = reversePath(rev_path, (len(maze)-2, len(maze[0])-2), loc)
        # print("The Plan: ", path)
        new_loc, explored_maze = executeAdapted(path, explored_maze, maze, loc)
        loc = new_loc
    print("Adapted Maze:")
    create.printMaze(explored_maze, h, w)
    
    return numExpanded