
import heapq
import mazes.maze as create
from pathfinding.adaptedA import adaptedDriver
from pathfinding.forwardA import AForwardDriver
import display

def main(command):
    # Initialize start of search
    # h = int(input())
    # w = int(input())
    h = 10
    w = 10

    maze = create.main(h, w)
    # display.main(maze, command)
    


         

    # forExpanded = AForwardDriver(maze)
    # adaptExpanded = adaptedDriver(maze)

    # print("forward expanded num: ", forExpanded)
    # print("adapted expanded num: ", adaptExpanded)

    print("maze solved")
    
    
