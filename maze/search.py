import heapq
import random
from collections import deque
from itertools import count
from .generator import DIRS
from .settings import TERRAIN_COST

def open_neighbors(grid, cell):
    c, r = cell
    result = []
    for i, (dx, dy) in enumerate(DIRS):
        if not grid[r][c][i]:
            result.append((c + dx, r + dy))
    return result

class Search:
    def __init__(self, grid, start, goal, algorithm, terrain):
        self.grid, self.goal, self.terrain = grid, goal, terrain
        self.algorithm = algorithm
        self.visited = set()
        self.came_from = {start: None}
        self.cost_so_far = {start: 0}
        self.current = None
        self.done = False
        self.found = False
        self.tiebreak = count()
        if algorithm == "dijkstra":
            self.frontier = [(0, next(self.tiebreak), start)]
        else:
            self.frontier = deque([start])

    def frontier_cells(self):
        if self.algorithm == "dijkstra":
            return [cell for (_, _, cell) in self.frontier]
        return list(self.frontier)

    def step(self):
        if self.done:
            return
        if not self.frontier:
            self.done = True
            return

        if self.algorithm == "bfs":
            self.current = self.frontier.popleft()
        elif self.algorithm == "dfs":
            self.current = self.frontier.pop()
        else:
            cost, _, cell = heapq.heappop(self.frontier)
            if cost > self.cost_so_far[cell]:
                return
            self.current = cell
        self.visited.add(self.current)

        if self.current == self.goal:
            self.done = self.found = True
            return

        neighbors = open_neighbors(self.grid, self.current)
        random.shuffle(neighbors)
        for nxt in neighbors:
            if self.algorithm == "dijkstra":
                new_cost = self.cost_so_far[self.current] + TERRAIN_COST[self.terrain[nxt]]
                if nxt not in self.cost_so_far or new_cost < self.cost_so_far[nxt]:
                    self.cost_so_far[nxt] = new_cost
                    self.came_from[nxt] = self.current
                    heapq.heappush(self.frontier, (new_cost, next(self.tiebreak), nxt))
            elif nxt not in self.came_from:
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

    def path_cost(self):
        return sum(TERRAIN_COST[self.terrain[cell]] for cell in self.path()[1:])