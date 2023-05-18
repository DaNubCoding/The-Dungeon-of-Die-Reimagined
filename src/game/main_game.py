from random import choice, randint
from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.tile import TileManager
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.tile_manager = TileManager(self)

    def update(self) -> None:
        super().update()

    def draw(self) -> None:
        super().draw()