from random import choice, randint
from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.tiles = [[randint(0, len(img.cobblestones) - 1) for _ in range(16)] for _ in range(12)]
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                while self.tiles[y][x] == self.tiles[y][x - 1] or self.tiles[y][x] == self.tiles[y - 1][x]:
                    self.tiles[y][x] = randint(0, len(img.cobblestones) - 1)
        self.cracks = [[Texture(self.manager.window, choice(img.cracks)) if randint(0, 1) else None for _ in range(16)] for _ in range(12)]
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                tile = img.cobblestones[self.tiles[y][x]].copy()
                if self.cracks[y][x]:
                    tile.blit(self.cracks[y][x].surf, (0, 0), special_flags=BLEND_RGB_SUB)
                self.tiles[y][x] = Texture(self.manager.window, tile)

    def update(self) -> None:
        super().update()

    def draw(self) -> None:
        super().draw()
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                self.manager.window.render(tile, (x * 64, y * 64))