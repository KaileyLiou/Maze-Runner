import pygame
from . import settings as S
from .generator import generate_maze, generate_terrain, build_walls
from .player import Player, cell_center
from .npc import SearchNPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        pygame.display.set_caption("BFS vs Dijkstra | brown = mud (3), blue = web (6) | SPACE = new maze")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 56)
        self.player = Player(S.ENTRANCE)
        self.bfs_npc = SearchNPC(S.ENTRANCE, "bfs", S.BFS_COLOR, "BFS (gold)", -3)
        self.dijkstra_npc = SearchNPC(S.ENTRANCE, "dijkstra", S.DIJKSTRA_COLOR, "Dijkstra (purple)", 3)
        self.npcs = [self.bfs_npc, self.dijkstra_npc]
        self.terrain_tiles = {}
        for name, color in S.TERRAIN_COLOR.items():
            tile = pygame.Surface((S.CELL, S.CELL))
            tile.fill(color)
            self.terrain_tiles[name] = tile
        self.new_maze()

    def new_maze(self):
        self.grid = generate_maze()
        self.terrain = generate_terrain()
        self.walls = build_walls(self.grid)
        self.player.reset()
        print("--- new maze ---")
        for npc in self.npcs:
            npc.start_search(self.grid, S.EXIT, self.terrain)
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
        for (c, r), name in self.terrain.items():
            if name in self.terrain_tiles:
                self.screen.blit(self.terrain_tiles[name], (c * S.CELL, r * S.CELL))
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