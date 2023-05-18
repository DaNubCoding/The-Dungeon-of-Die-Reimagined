from random import choice, randint
from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.tile import TileManager
from src.game.player import Player
from src.game.camera import Camera
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.player = Player(self)
        self.camera = Camera(self, self.player)
        self.tile_manager = TileManager(self)

    def update(self) -> None:
        self.camera.update()
        super().update()

    def draw(self) -> None:
        self.manager.window.fill((0, 0, 0))
        super().draw()