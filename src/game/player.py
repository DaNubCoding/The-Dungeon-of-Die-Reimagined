from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class Player(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.PLAYER)
        self.size = VEC(48, 48)
        self.image = pygame.Surface(self.size)
        self.image.fill((255, 0, 0))
        self.image = Texture(self.manager.window, self.image)
        self.pos = VEC(0, 0)

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.pos.y -= 3 * self.manager.dt
        if keys[K_s]:
            self.pos.y += 3 * self.manager.dt
        if keys[K_a]:
            self.pos.x -= 3 * self.manager.dt
        if keys[K_d]:
            self.pos.x += 3 * self.manager.dt

    def draw(self) -> None:
        self.manager.window.render(self.image, self.pos - self.scene.camera.pos)