# https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96

import matplotlib.pyplot as plt
import numpy as np
import random
from queue import Queue
from colorama import init
from colorama import Fore, Back, Style

def printMaze(maze, height, width):
	for i in range(0, height):
		for j in range(0, width):
			if (maze[i][j] == '?'):
				print(Fore.WHITE + str(maze[i][j]), end=" ")
			elif (maze[i][j] == 0):
				print(Fore.GREEN + str(maze[i][j]), end=" ")
			else:
				print(Fore.RED + str(maze[i][j]), end=" ")
			
		print('\n')

def create_maze(dim):
    # Create a grid filled with walls
    maze = np.ones((dim*2+1, dim*2+1))

    # Define the starting point
    x, y = (0, 0)
    maze[2*x+1, 2*y+1] = 0

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] == 1:
                maze[2*nx+1, 2*ny+1] = 0
                maze[2*x+1+dx, 2*y+1+dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
            
    # Create an entrance and an exit
    maze[1, 0] = 0
    maze[-2, -1] = 0

    return maze

m = create_maze(5)

printMaze(m, 11, 11)