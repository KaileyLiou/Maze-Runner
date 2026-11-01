import pygame
from . import settings as S
from .generator import generate_maze, build_walls
from .player import Player, cell_center
from .npc import SearchNPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        pygame.display.set_caption("DFS vs BFS | SPACE = new maze, arrows/WASD = move")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 56)
        self.player = Player(S.ENTRANCE)
        self.bfs_npc = SearchNPC(S.ENTRANCE, True, S.BFS_COLOR, "BFS (gold)", -3)
        self.dfs_npc = SearchNPC(S.ENTRANCE, False, S.DFS_COLOR, "DFS (purple)", 3)
        self.npcs = [self.bfs_npc, self.dfs_npc]
        self.new_maze()

    def new_maze(self):
        self.grid = generate_maze()
        self.walls = build_walls(self.grid)
        self.player.reset()
        for npc in self.npcs:
            npc.start_search(self.grid, S.EXIT)
        self.winner = None

    def goal_rect(self):
        cx, cy = cell_center(S.EXIT)
        return pygame.Rect(cx - S.CELL // 2 + 4, cy - S.CELL // 2 + 4, S.CELL - 8, S.CELL - 8)

    def update(self):
        self.player.update(self.walls)
        for npc in self.npcs:
            npc.update()
        if not self.winner:
            goal = self.goal_rect()
            if self.player.rect.colliderect(goal):
                self.winner = "You reached the goal first!"
            for npc in self.npcs:
                if npc.rect.colliderect(goal) and npc.search.done:
                    self.winner = f"{npc.name} reached the goal first!"
                    break

    def draw(self):
        self.screen.fill(S.BG)
        for npc in self.npcs:
            npc.draw_search(self.screen)
        sx, sy = cell_center(S.ENTRANCE)
        pygame.draw.rect(self.screen, S.START_COLOR,
                         (sx - S.CELL // 2 + 4, sy - S.CELL // 2 + 4, S.CELL - 8, S.CELL - 8), 3)
        pygame.draw.rect(self.screen, S.GOAL_COLOR, self.goal_rect())
        self.walls.draw(self.screen)
        for npc in self.npcs:
            self.screen.blit(npc.image, npc.rect)
        self.screen.blit(self.player.image, self.player.rect)

        if self.winner:
            text = self.font.render(self.winner, True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(S.WIDTH // 2, S.HEIGHT // 2)))
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