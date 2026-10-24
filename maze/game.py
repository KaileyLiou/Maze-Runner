import pygame
from . import settings as S
from .generator import generate_maze, build_walls
from .player import Player, cell_center
from .npc import NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 56)
        self.player = Player(S.ENTRANCE)
        self.npc = NPC(S.ENTRANCE)
        self.new_maze()

    def new_maze(self):
        self.grid = generate_maze()
        self.walls = build_walls(self.grid)
        self.player.reset()
        self.npc.plan(self.grid, S.EXIT)
        self.winner = None

    def goal_rect(self):
        cx, cy = cell_center(S.EXIT)
        return pygame.Rect(cx - S.CELL, cy - S.CELL, S.CELL - 8, S.CELL - 8)

    def update(self):
        if self.winner:
            return
        self.player.update(self.walls)
        self.npc.update()
        goal = self.goal_rect()
        if self.player.rect.colliderect(goal):
            self.winner = "You win!"
        elif self.npc.rect.colliderect(goal):
            self.winner = "NPC wins!"

    def draw(self):
        self.screen.fill(S.BG)
        sx, sy = cell_center(S.ENTRANCE)
        pygame.draw.rect(self.screen, S.START_COLOR, (sx - S.CELL, sy - S.CELL, S.CELL - 8, S.CELL - 8))
        pygame.draw.rect(self.screen, S.GOAL_COLOR, self.goal_rect())
        self.walls.draw(self.screen)
        self.screen.blit(self.npc.image, self.npc.rect)
        self.screen.blit(self.player.image, self.player.rect)
        if self.winner:
            text = self.font.render(self.winner + "  (SPACE = new maze)", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(S.WIDTH, S.HEIGHT)))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.new_maze()
            self.update()
            self.draw()
            self.clock.tick(S.FPS)
        pygame.quit()
