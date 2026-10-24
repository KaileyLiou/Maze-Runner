import pygame
from .settings import WALL_COLOR

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
