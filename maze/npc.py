import pygame
from .settings import CELL, PLAYER_SIZE, NPC_SPEED, SEARCH_STEPS_PER_FRAME
from .player import cell_center
from .search import Search

class SearchNPC(pygame.sprite.Sprite):

    def __init__(self, cell, algorithm, color, name, path_offset):
        super().__init__()
        self.start, self.color, self.name = cell, color, name
        self.algorithm = algorithm
        self.path_offset = path_offset
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, PLAYER_SIZE, PLAYER_SIZE), border_radius=5)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, PLAYER_SIZE, PLAYER_SIZE), 2, border_radius=5)
        self.rect = self.image.get_rect(center=cell_center(cell))
        self.tile_visited = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        self.tile_visited.fill((*color, 30))
        self.tile_frontier = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        self.tile_frontier.fill((*color, 120))
        self.font = pygame.font.SysFont(None, 20)
        self.search = None
        self.walk = []
        self.reported = False

    def start_search(self, grid, goal, terrain):
        self.rect.center = cell_center(self.start)
        self.search = Search(grid, self.start, goal, self.algorithm, terrain)
        self.walk = []
        self.reported = False

    def update(self):
        s = self.search
        if not s.done:
            for _ in range(SEARCH_STEPS_PER_FRAME):
                s.step()
            if s.done:
                self.walk = s.path()[1:]
                self.report()
            return
        if self.walk:
            tx, ty = cell_center(self.walk[0])
            cx, cy = self.rect.center
            dx = max(-NPC_SPEED, min(NPC_SPEED, tx - cx))
            dy = max(-NPC_SPEED, min(NPC_SPEED, ty - cy))
            self.rect.center = (cx + dx, cy + dy)
            if self.rect.center == (tx, ty):
                self.walk.pop(0)

    def report(self):
        s = self.search
        print(f"{self.name}: steps = {len(s.path()) - 1}, total cost = {s.path_cost()}, "
              f"nodes explored = {len(s.visited)}")

    def draw_search(self, surface):
        s = self.search
        for (c, r) in s.visited:
            surface.blit(self.tile_visited, (c * CELL, r * CELL))
        for (c, r) in s.frontier_cells():
            surface.blit(self.tile_frontier, (c * CELL, r * CELL))
        if not s.done and s.current:
            c, r = s.current
            pygame.draw.rect(surface, (255, 255, 255), (c * CELL + 4, r * CELL + 4, CELL - 8, CELL - 8), 3)
        if s.algorithm == "dijkstra":
            for (c, r) in s.visited:
                label = self.font.render(str(s.cost_so_far[(c, r)]), True, (255, 255, 255))
                surface.blit(label, (c * CELL + 4, r * CELL + 4))
        if s.found:
            o = self.path_offset
            pts = [(cell_center(p)[0] + o, cell_center(p)[1] + o) for p in s.path()]
            if len(pts) > 1:
                pygame.draw.lines(surface, self.color, False, pts, 4)