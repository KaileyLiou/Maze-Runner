import random
import pygame
from .settings import CELL, WALL, COLS, ROWS
from .wall import Wall

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def generate_maze(cols=COLS, rows=ROWS):
    grid = [[[True] * 4 for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    x, y = random.randrange(cols), random.randrange(rows)
    visited[y][x] = True
    stack = []

    while True:
        unvisited = []
        for i, (dx, dy) in enumerate(DIRS):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                unvisited.append((i, nx, ny))

        if unvisited:
            i, nx, ny = random.choice(unvisited)
            grid[y][x][i] = False
            grid[ny][nx][(i + 2) % 4] = False
            stack.append((x, y))
            visited[ny][nx] = True
            x, y = nx, ny
        elif stack:
            x, y = stack.pop()
        else:
            break

    return grid

def build_walls(grid):
    group = pygame.sprite.Group()
    rows, cols = len(grid), len(grid[0])
    half = WALL // 2
    for r in range(rows):
        for c in range(cols):
            x, y = c * CELL, r * CELL
            top, right, bottom, left = grid[r][c]
            if top:
                group.add(Wall(x - half, y - half, CELL + WALL, WALL))
            if left:
                group.add(Wall(x - half, y - half, WALL, CELL + WALL))
            if right and c == cols - 1:
                group.add(Wall(x + CELL - half, y - half, WALL, CELL + WALL))
            if bottom and r == rows - 1:
                group.add(Wall(x - half, y + CELL - half, CELL + WALL, WALL))
    return group