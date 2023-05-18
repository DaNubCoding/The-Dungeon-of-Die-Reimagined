from random import randint, choice
from pygame.locals import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class TileManager:
    def __init__(self, scene: Scene) -> None:
        self.tiles = [[[randint(0, len(img.cobblestones) - 1), randint(0, len(img.cracks) - 1)] for _ in range(16)] for _ in range(12)]
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x][0] == self.tiles[y - 1][x][0]:
                    self.tiles[y][x][0] = choice([i for i in range(len(img.cobblestones)) if i != self.tiles[y - 1][x][0]])
                if self.tiles[y][x][0] == self.tiles[y][x - 1][0]:
                    self.tiles[y][x][0] = choice([i for i in range(len(img.cobblestones)) if i != self.tiles[y][x - 1][0]])
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                image = img.cobblestones[self.tiles[y][x][0]].copy()
                crack = img.cracks[self.tiles[y][x][1]]
                image.blit(crack, (0, 0), special_flags=BLEND_RGB_SUB)
                Tile(scene, Layers.FLOOR, Texture(scene.manager.window, image), (x * 64, y * 64))

class Tile(Sprite):
    def __init__(self, scene: Scene, layer: Layers, image: Texture, pos: tuple[int, int]) -> None:
        super().__init__(scene, layer)
        self.image = image
        self.pos = VEC(pos)

    def draw(self) -> None:
        self.manager.window.render(self.image, self.pos)