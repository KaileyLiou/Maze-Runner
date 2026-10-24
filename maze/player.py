import pygame
from .settings import CELL, PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR

class Player(pygame.sprite.Sprite):
    def __init__(self, cell):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (PLAYER_SIZE // 2, PLAYER_SIZE // 2), PLAYER_SIZE // 2)
        self.rect = self.image.get_rect(center=cell_center(cell))
        self.start = cell

    def reset(self):
        self.rect.center = cell_center(self.start)

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        self.move(dx * PLAYER_SPEED, dy * PLAYER_SPEED, walls)

    def move(self, dx, dy, walls):
        self.rect.x += dx
        for w in pygame.sprite.spritecollide(self, walls, False):
            if dx > 0:
                self.rect.right = w.rect.left
            elif dx < 0:
                self.rect.left = w.rect.right
        self.rect.y += dy
        for w in pygame.sprite.spritecollide(self, walls, False):
            if dy > 0:
                self.rect.bottom = w.rect.top
            elif dy < 0:
                self.rect.top = w.rect.bottom

def cell_center(cell):
    c, r = cell
    return (c * CELL + CELL // 2, r * CELL + CELL // 2)
