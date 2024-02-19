import heapq
import maze as create
maze = create.main()

class PriorityQueue(object):
    def __init__(self) -> None:
        self.heap = []
        self._index = 0 # For identical priorities

    def __str__(self) -> str:
        # return ' '.join(tuple(self.heap))
        return ' '.join(map(str, self.heap))
    
    def empty(self):
        return len(self.heap) == 0
    
    def add(self, element, priority):
        heapq.heappush(self.heap, (priority, self._index, element))
        self._index += 1

    def remove(self):
        return heapq.heappop(self.heap)[-1]
            



def BasicA(maze, start):
    # Eval Function: f(n) = g(n) + h(n)
    # f(n) - Estimated cost of cheapest solution through n
    # g(n) - path cost from start node to node n
    # h(n) - estimated cost of cheapest path from n to the goal (Manhattan distance). Curr Grid --> [101,100] 
    frontier = PriorityQueue()
    running_cost = {}
    prev_loc = {}
    close_list = []

    frontier.add(start, 0)
    running_cost[start] = 0
    prev_loc[start] = None

    while not frontier.empty():
        curr_loc = frontier.remove()
        print("new cell")
        print(curr_loc)
        print(maze[curr_loc[0]][curr_loc[1]])
        print("frontier", frontier)
        print("running cost", running_cost)
        print("close list", close_list)
        close_list.append(curr_loc)
        
        # If reach goal, break
        if curr_loc == (101,100):
            break
        # If hit a wall, break
        if maze[curr_loc[0]][curr_loc[1]] == 'w':
            break

        # Check four directions
        # Only add to frontier if not in closed list (hasn't been visited)
        g = running_cost[curr_loc]+1
        # Top
        if curr_loc[0] > 1 and (curr_loc[0]-1, curr_loc[1]) not in close_list:
            heuristic = abs((len(maze)-1) - (curr_loc[0]-1)) + abs((len(maze[0])-2) - curr_loc[1])
            frontier.add((curr_loc[0]-1, curr_loc[1]), g+heuristic)
            running_cost[(curr_loc[0]-1, curr_loc[1])] = g
            prev_loc[(curr_loc[0]-1, curr_loc[1])] = curr_loc

        # Bottom
        if curr_loc[0] < len(maze)-2 and (curr_loc[0]+1, curr_loc[1]) not in close_list:
            heuristic = abs((len(maze)-1) - (curr_loc[0]+1)) + abs((len(maze[0])-2) - curr_loc[1])
            frontier.add((curr_loc[0]+1, curr_loc[1]), g+heuristic)
            running_cost[(curr_loc[0]+1, curr_loc[1])] = g
            prev_loc[(curr_loc[0]+1, curr_loc[1])] = curr_loc
        # Left
        if curr_loc[1] > 1 and (curr_loc[0], curr_loc[1]-1) not in close_list:
            heuristic = abs((len(maze)-1) - (curr_loc[0])) + abs(len(maze[0])-2 - curr_loc[1]-1)
            frontier.add((curr_loc[0], curr_loc[1]-1), g+heuristic)
            running_cost[(curr_loc[0], curr_loc[1]-1)] = g
            prev_loc[(curr_loc[0], curr_loc[1]-1)] = curr_loc
        # Right
        if curr_loc[1] < len(maze[0])-2 and (curr_loc[0], curr_loc[1]+1) not in close_list:
            heuristic = abs((len(maze)-1) - (curr_loc[0])) + abs(len(maze[0])-2 - curr_loc[1]+1)
            frontier.add((curr_loc[0], curr_loc[1]+1), g+heuristic)
            running_cost[(curr_loc[0], curr_loc[1]+1)] = g
            prev_loc[(curr_loc[0], curr_loc[1]+1)] = curr_loc
        
    return prev_loc[curr_loc]







def main():
    # Initialize start of search
    counter = 0
    # Call A* whenever run into a wall
    cell = BasicA(maze, (0,1))
    print(cell)
    # while cell != (len(maze), len(maze[0])-1):
    #     ComputePath(maze, cell)
    print("maze solved")
    

main()
    
