from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.surface = pygame.Surface((100, 100), SRCALPHA)
        self.surface.fill((255, 0, 0))
        self.texture = Texture(self.manager.window, self.surface)

    def update(self) -> None:
        # here
        super().update()
        # or here

    def draw(self) -> None:
        super().draw()

        self.manager.window.fill((25, 25, 25))
        self.manager.window.render(self.texture, (100, 100))