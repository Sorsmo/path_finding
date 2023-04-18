import numpy as np
import pygame as py
import random as rand
import time
import sys
from pygame.locals import *

HEIGHT = 750
WIDTH = 750
ACTUAL_WIDTH = 900
TILE_STEP = 15 # lower means less squares
tile_width = int(WIDTH/TILE_STEP)
tile_height = int(HEIGHT/TILE_STEP)

def BFS(screen, grid):
    rows, cols = grid.shape
    start = (0, 0)
    end = (rows - 1, cols - 1)
    queue = [start]
    visited = [start]
    previous = [-1 for i in range(TILE_STEP ** 2)]
    color = [1, 0, 0]
    while queue:
        row, col = queue.pop(0)
        if (row, col) == end:
            # visited.append((row, col))
            # previous[row * grid.shape[0] + col] = (row, col)
            break
        i = 0
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and (r, c) not in visited:
                queue.append((r, c))
                visited.append((r, c))
                previous[r * grid.shape[0] + c] = i

                if (r,c) != (0, 0) and (r,c) != (rows - 1,cols - 1):
                    color2 = (color[0], color[1], color[2])
                    py.draw.rect(screen, color2, py.Rect(c*tile_width, r*tile_width, tile_width, tile_width))
                    if color[0] < 254:
                        color[0] += 1
            i += 1
        py.time.delay(10)
        py.display.flip()
    
    end_x = grid.shape[0] - 1
    end_y = grid.shape[1] - 1
    
    if previous[end_y * grid.shape[0] + end_x - 1] != -1:
        end_idx = end_y * grid.shape[0] + end_x - 1
        while end_idx != 0:
            py.draw.rect(screen, (0, 0, 255), py.Rect((end_idx % grid.shape[0])*tile_width, (end_idx // grid.shape[0])*tile_height, tile_width, tile_width))
            if previous[end_idx] == 0:      # go up
                end_idx += (grid.shape[1])
            if previous[end_idx] == 1:      # go down
                end_idx -= (grid.shape[1])
            if previous[end_idx] == 2:      # go left
                end_idx += 1
            if previous[end_idx] == 3:      # go right
                end_idx -= 1
            
            py.time.delay(30)
            py.display.flip()
    elif previous[end_y * grid.shape[0] + end_x - grid.shape[0]] != -1:
        end_idx = end_y * grid.shape[0] + end_x - grid.shape[0]
        while end_idx != 0:
            py.draw.rect(screen, (0, 0, 255), py.Rect((end_idx % grid.shape[0])*tile_width, (end_idx // grid.shape[0])*tile_height, tile_width, tile_width))
            if previous[end_idx] == 0:      # go up
                end_idx += (grid.shape[1])
            if previous[end_idx] == 1:      # go down
                end_idx -= (grid.shape[1])
            if previous[end_idx] == 2:      # go left
                end_idx += 1
            if previous[end_idx] == 3:      # go right
                end_idx -= 1
            
            py.time.delay(30)
            py.display.flip()


def DFS(screen, grid):
    rows, cols = grid.shape
    start = (0, 0)
    end = (rows - 1, cols - 1)
    stack = [start]
    visited = set(start)
    color = [1, 0, 0]
    while stack:
        row, col = stack.pop()
        if (row, col) == end:
            break
        found_end = False
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)][::-1]:
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0 and (r, c) not in visited:
                stack.append((r, c))
                visited.add((r, c))
                if (r,c) != (0, 0) and (r,c) != (rows - 1,cols - 1):
                    color2 = (color[0], color[1], color[2])
                    py.draw.rect(screen, color2, py.Rect(c*tile_width, r*tile_width, tile_width, tile_width))
                    if color[0] < 254:
                        color[0] += 1
                if (r, c) == end:
                    found_end = True
                    break
        if found_end:
            break
        py.time.delay(10)
        py.display.flip()

    
def setup_screen(screen, grid):
    for i in range(grid.shape[0]):
        grid[i,:] = 0
    for i in range(0, HEIGHT, tile_height):
        for j in range(0, WIDTH, tile_width):
            py.draw.rect(screen, (80,80,80), py.Rect(j, i, tile_height, tile_width))
    py.draw.rect(screen, (0, 200, 0), py.Rect(0, 0, tile_height, tile_width)) # start tile
    py.draw.rect(screen, (0, 200, 0), py.Rect(HEIGHT - tile_height, WIDTH - tile_width, tile_height, tile_width)) # finish tile

def main():
    py.init()
    font = py.font.SysFont('Arial', 25)

    screen = py.display.set_mode((ACTUAL_WIDTH, HEIGHT))
    py.display.set_caption('Path Finding by Sorsmo')

    grid = np.zeros((TILE_STEP, TILE_STEP))
   
    # setup screen
    setup_screen(screen, grid)
        
    # buttons
    start_button = (WIDTH+10, 10)
    py.draw.rect(screen, (10, 100, 55), py.Rect(WIDTH, tile_height*0, ACTUAL_WIDTH-WIDTH, tile_height))
    screen.blit(font.render('BFS', True, (255,255,255)), start_button)

    start_button = (WIDTH+10, 10+tile_height)
    py.draw.rect(screen, (10, 100, 55), py.Rect(WIDTH, tile_height*1, ACTUAL_WIDTH-WIDTH, tile_height))
    screen.blit(font.render('DFS', True, (255,255,255)), start_button)

    clear_button = (WIDTH+10, 10+tile_height*2)
    py.draw.rect(screen, (100, 10, 55), py.Rect(WIDTH, tile_height*2, ACTUAL_WIDTH-WIDTH, tile_height))
    screen.blit(font.render('Clear', True, (255,255,255)), clear_button)

    py.display.flip()
    running = True
    dragging = False
    searched = False
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                dragging = True
                if WIDTH < py.mouse.get_pos()[0] < ACTUAL_WIDTH and tile_height*0 <= py.mouse.get_pos()[1] < tile_height:
                    BFS(screen, grid)
                    searched = True
                elif WIDTH < py.mouse.get_pos()[0] < ACTUAL_WIDTH and tile_height*1 <= py.mouse.get_pos()[1] < tile_height*2:
                    DFS(screen, grid)
                    searched = True
                elif WIDTH < py.mouse.get_pos()[0] < ACTUAL_WIDTH and tile_height*2 <= py.mouse.get_pos()[1] < tile_height*3:
                    setup_screen(screen, grid)
                    searched = False
            elif event.type == py.MOUSEBUTTONUP:
                dragging = False
                mouse_pos = py.mouse.get_pos()
                x = mouse_pos[1]//tile_height
                y = mouse_pos[0]//tile_width
                if x < WIDTH and y < HEIGHT and not searched:
                    if (x,y) != (0,0) and (x,y) != (TILE_STEP - 1, TILE_STEP - 1) and x < TILE_STEP and y < TILE_STEP:
                        color = (255, 255, 0)
                        py.draw.rect(screen, color, py.Rect(y*tile_height, x*tile_width, tile_height, tile_width))
                        grid[x][y] = 1
            elif event.type == py.MOUSEMOTION:
                if dragging and not searched:
                    mouse_pos = py.mouse.get_pos()
                    x = mouse_pos[1]//tile_height
                    y = mouse_pos[0]//tile_width
                    if (x,y) != (0,0) and (x,y) != (TILE_STEP - 1, TILE_STEP - 1) and x < TILE_STEP and y < TILE_STEP:
                        color = (255, 255, 0)
                        py.draw.rect(screen, color, py.Rect(y*tile_height, x*tile_width, tile_height, tile_width))
                        grid[x][y] = 1
        py.display.flip()
main()