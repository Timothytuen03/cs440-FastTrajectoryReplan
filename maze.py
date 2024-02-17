# Maze Alg: https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
# https://github.com/OrWestSide/python-scripts/blob/master/maze.py
# Wikipedia: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Kruskal's_algorithm_(with_sets)
# Prim's Alg: https://en.wikipedia.org/wiki/Prim%27s_algorithm

import random
import time
from colorama import init
from colorama import Fore, Back, Style

walls = []
def init_maze(ylen, xlen):
    maze = [['?' for _ in range(xlen)] for _ in range(ylen)]
    printMaze(maze, ylen, xlen)
    return maze
# Functions
def printMaze(maze, height, width):
	for i in range(0, height):
		for j in range(0, width):
			if (maze[i][j] == '?'):
				print(Fore.WHITE + str(maze[i][j]), end=" ")
			elif (maze[i][j] == 'p'):
				print(Fore.GREEN + str(maze[i][j]), end=" ")
			else:
				print(Fore.RED + str(maze[i][j]), end=" ")
			
		print('\n')

def create_maze(height, width, maze):
    start_y = int(random.random()*height)
    start_x = int(random.random()*width)
    print(start_x, start_x)
    if start_y == 0:
        start_y += 1
    if start_y == height-1:
        start_y -= 1
    if start_x == 0:
        start_x += 1
    if start_x == width-1:
        start_x -= 1
    print(start_x, start_y)
    # Starting Point
    maze[start_x][start_y] = 'p'
    walls.append((start_x-1, start_y))
    walls.append((start_x+1, start_y))
    walls.append((start_x, start_y-1))
    walls.append((start_x, start_y+1))
    maze[start_y+1][start_x] = 'w'
    maze[start_y-1][start_x] = 'w'
    maze[start_y][start_x+1] = 'w'
    maze[start_y][start_x-1] = 'w'

    print("make da walls")
    make_walls(height,width, maze)
    print("fill da leftova")
    leftovers(height, width, maze)
    print("make da entrance")
    create_entrance_exit(height, width, maze)
    print("print da maze!")
    # print_maze(maze)
                

def make_walls(height, width, maze):
    # Walls!
    while walls:
        # print("still building...")
        # Pick a random wall
        # rand_wall_num = random.randint(0,len(walls)) - 1
        rand_wall_num = int(random.random()*len(walls))-1
        rand_wall = walls[rand_wall_num]
        print(walls)
        print(rand_wall)
        # Check if wall is between two paths
        # 
        if rand_wall[0] != height-1:
            if maze[rand_wall[0]-1][rand_wall[1]] == 'p' and maze[rand_wall[0]+1][rand_wall[1]] == '?':
                s_cells = surroundingCells(rand_wall, maze)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = 'p'
                
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if maze[rand_wall[0]][rand_wall[1]-1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                delete_wall(rand_wall, maze)
                continue

        if rand_wall[0] != 0:
            if maze[rand_wall[0]-1][rand_wall[1]] == '?' and maze[rand_wall[0]+1][rand_wall[1]] == 'p':
                s_cells = surroundingCells(rand_wall, maze)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = 'p'
                
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if maze[rand_wall[0]][rand_wall[1]-1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                delete_wall(rand_wall, maze)
                continue

        if rand_wall[1] != width-1:
            if maze[rand_wall[0]][rand_wall[1]-1] == 'p' and maze[rand_wall[0]][rand_wall[1]+1] == '?':
                s_cells = surroundingCells(rand_wall, maze)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = 'p'
                
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                delete_wall(rand_wall, maze)
                continue

        if rand_wall[1] != 0:                
            if maze[rand_wall[0]][rand_wall[1]-1] == '?' and maze[rand_wall[0]][rand_wall[1]+1] == 'p':
                s_cells = surroundingCells(rand_wall, maze)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = 'p'
                
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'p':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if maze[rand_wall[0]][rand_wall[1]-1] != 'p':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                delete_wall(rand_wall, maze)
                continue
        delete_wall(rand_wall, maze)

def surroundingCells(rand_wall, maze):
    s_cells = 0
    if (maze[rand_wall[0]-1][rand_wall[1]] == 'p'):
        s_cells += 1
    if (maze[rand_wall[0]+1][rand_wall[1]] == 'p'):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]-1] == 'p'):
        s_cells +=1
    if (maze[rand_wall[0]][rand_wall[1]+1] == 'p'):
        s_cells += 1
    return s_cells

def delete_wall(rand_wall, maze):
    # print("deleting wall")
    for wall in walls:
        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
            walls.remove(wall) 

def leftovers(height, width, maze):
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == '?'):
                maze[i][j] = 'w'

def create_entrance_exit(height, width, maze):
    for i in range(0, width):
        if (maze[1][i] == 'p'):
            maze[0][i] = 'p'
            break
    for i in range(width-1, 0, -1):
        if (maze[height-2][i] == 'p'):
            maze[height-1][i] = 'p'
            break


def main():
    h = int(input())
    w = int(input())
    maze = init_maze(h, w)
    create_maze(h, w, maze)
    printMaze(maze, h, w)
    return maze