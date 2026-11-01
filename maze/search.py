import random
from collections import deque
from .generator import DIRS

def open_neighbors(grid, cell):
    c, r = cell
    result = []
    for i, (dx, dy) in enumerate(DIRS):
        if not grid[r][c][i]:
            result.append((c + dx, r + dy))
    return result

class Search:
    def __init__(self, grid, start, goal, use_queue):
        self.grid = grid
        self.goal = goal
        self.use_queue = use_queue
        self.frontier = deque([start])
        self.visited = set()
        self.came_from = {start: None}
        self.current = None
        self.done = False
        self.found = False

    def step(self):
        if self.done:
            return
        if not self.frontier:
            self.done = True
            return

        if self.use_queue:
            self.current = self.frontier.popleft()
        else:
            self.current = self.frontier.pop()
        self.visited.add(self.current)

        if self.current == self.goal:
            self.done = self.found = True
            return

        neighbors = open_neighbors(self.grid, self.current)
        random.shuffle(neighbors)
        for nxt in neighbors:
            if nxt not in self.came_from:
                self.came_from[nxt] = self.current
                self.frontier.append(nxt)

    def path(self):
        if not self.found:
            return []
        path, cell = [], self.goal
        while cell is not None:
            path.append(cell)
            cell = self.came_from[cell]
        return path[::-1]