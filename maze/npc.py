import pygame
from .settings import PLAYER_SIZE, NPC_SPEED, NPC_COLOR
from .generator import solve_bfs
from .player import cell_center

class NPC(pygame.sprite.Sprite):
    def __init__(self, cell):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, NPC_COLOR, (0, 0, PLAYER_SIZE, PLAYER_SIZE),
                         border_radius=5)
        self.rect = self.image.get_rect(center=cell_center(cell))
        self.start = cell
        self.path = []

    def plan(self, grid, goal):
        self.rect.center = cell_center(self.start)
        self.path = solve_bfs(grid, self.start, goal)[1:]

    def update(self):
        if not self.path:
            return
        tx, ty = cell_center(self.path[0])
        cx, cy = self.rect.center
        step = NPC_SPEED
        dx = max(-step, min(step, tx - cx))
        dy = max(-step, min(step, ty - cy))
        self.rect.center = (cx + dx, cy + dy)
        if self.rect.center == (tx, ty):
            self.path.pop(0)
