import pygame

import sys
import numpy as np
import random

from menu import Button

from algorithms import dfs, bfs

from constants import *

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}

class Maze:

    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [[Cell(x, y) for y in range(self.grid_height)] for x in range(self.grid_width)]

    def reset_maze(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False
                # cell.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}

    def get_neighbors(self, cell):
        neighbors = []

        if cell.x > 0:
            neighbors.append(self.grid[cell.x - 1][cell.y]) # Left neighbor
        
        if cell.x < self.grid_width - 1:
            neighbors.append(self.grid[cell.x + 1][cell.y]) # Right neighbor
        
        if cell.y > 0:
            neighbors.append(self.grid[cell.x][cell.y - 1]) # Top neighbor

        if cell.y < self.grid_height - 1:
            neighbors.append(self.grid[cell.x][cell.y + 1]) # Bottom neighbor
        
        return [n for n in neighbors if not n.visited]

    def check_wall(self, first_cell, second_cell):
        dx = second_cell.x - first_cell.x
        dy = second_cell.y - first_cell.y

        if dx > 0: # Right neighbor
            return not first_cell.walls['right']
        
        elif dx < 0: # Left neighbor
            return not first_cell.walls['left']
        
        elif dy > 0: # Bottom neighbor
            return not first_cell.walls['bottom']
        
        else:
            return not first_cell.walls['top']

class MazeGenerator:

    def __init__(self, maze):
        self.maze = maze

    def generate_maze(self):
        stack = []
        start_cell = self.maze.grid[0][0]
        stack.append(start_cell)

        start_cell.visited = True
        while stack:
            current_cell = stack[-1]
            neighbors = self.maze.get_neighbors(current_cell)

            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_wall(current_cell, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            
            else:
                stack.pop()

    def remove_wall(self, current, next):
        dx = next.x - current.x
        dy = next.y - current.y

        if dx > 0: # Right neighbor
            current.walls['right'] = False
            next.walls['left'] = False
        
        elif dx < 0: # Left neighbor
            current.walls['left'] = False
            next.walls['right'] = False
        
        elif dy > 0: # Bottom neighbor
            current.walls['bottom'] = False
            next.walls['top'] = False
        
        else:
            current.walls['top'] = False
            next.walls['bottom'] = False

class Visualizer:

    def __init__(self, screen, maze):
        self.screen = screen
        self.maze = maze

    def draw_grid(self):
        for row in self.maze.grid:
            for cell in row:
                self.draw_cell(cell)

    def draw_cell(self, cell, color=None):
        x = cell.x * CELL_SIZE
        y = cell.y * CELL_SIZE

        if color:
            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        
        else:
            if cell.walls['top']:
                pygame.draw.line(self.screen, WHITE, (x, y), (x + CELL_SIZE, y))
            
            if cell.walls['bottom']:
                pygame.draw.line(self.screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))

            if cell.walls['left']:
                pygame.draw.line(self.screen, WHITE, (x, y), (x, y + CELL_SIZE))

            if cell.walls['right']:
                pygame.draw.line(self.screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))

    def draw_start_end_cell(self):
        pygame.draw.rect(self.screen, RED, (0, 0, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, GREEN, (GRID_WIDTH * CELL_SIZE - CELL_SIZE, GRID_HEIGHT * CELL_SIZE - CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def draw_final_path_cell(self, cell):
        x = cell.x * CELL_SIZE
        y = cell.y * CELL_SIZE

        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2

        pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), CELL_SIZE // 5)
    
    def update_display(self):
        pygame.display.update()

def create_buttons(algorithms):
    button_list = []
    x, y = MENU_START

    for algo in algorithms:
        button_list.append(Button(x, y, algo, algorithms[algo]))
        x += SPACING + BUTTON_WIDTH

    return button_list

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Maze')
    font = pygame.font.SysFont('arial', 15)

    maze = Maze(GRID_WIDTH, GRID_HEIGHT)
    generator = MazeGenerator(maze)
    visualizer = Visualizer(screen, maze)

    generator.generate_maze()
    maze.reset_maze()

    screen.fill(BLACK)
    visualizer.draw_grid()
    visualizer.draw_start_end_cell()

    algorithms = {
        'dfs': lambda: dfs.dfs(maze, start, end, visualizer),
        'bfs': lambda: bfs.bfs(maze, start, end, visualizer),
    }

    buttons = create_buttons(algorithms)
    for button in buttons:
        button.draw(screen, font)

    start = (0, 0)
    end = (maze.grid_width - 1, maze.grid_height - 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.check_click(pos)
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

        pygame.display.update()

if __name__ == '__main__':
    main()