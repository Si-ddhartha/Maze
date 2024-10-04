import pygame
from collections import deque
import time

def bfs(maze, start, end, visualizer):
    q = deque([maze.grid[start[0]][start[1]]])
    visited = set()
    parent_map = {}

    while q:
        current = q.popleft()

        if current in visited:
            continue

        visited.add(current)

        visualizer.draw_cell(current, color = (255, 0, 0))
        visualizer.update_display()

        if current.x == end[0] and current.y == end[1]:
            break

        neighbors = maze.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited and maze.check_wall(current, neighbor):
                q.append(neighbor)
                parent_map[neighbor] = current
                time.sleep(0.05)

        visualizer.draw_cell(current, color = (0, 0, 255))
        visualizer.update_display()
    
    if maze.grid[end[0]][end[1]] not in parent_map:
        return False  # No valid path was found

    path = []
    current = maze.grid[end[0]][end[1]]
    while current != maze.grid[start[0]][start[1]]:
        path.append(current)
        current = parent_map.get(current, None)  # Move to the parent cell

    path.append(maze.grid[start[0]][start[1]])
    path.reverse() 

    for cell in path:
        visualizer.draw_final_path_cell(cell)
        visualizer.update_display()
        time.sleep(0.02)

    return True
