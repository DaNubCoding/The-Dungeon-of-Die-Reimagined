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
        self.vel = VEC(0, 0)
        self.speed = 3
        self.rot_speed = 1
        self.rot = 0

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        self.vel = VEC(0, 0)
        if keys[K_w]:
            self.vel.y -= self.speed
        if keys[K_s]:
            self.vel.y += self.speed
        if keys[K_a]:
            self.vel.x -= self.speed
        if keys[K_d]:
            self.vel.x += self.speed
        self.pos += self.vel * self.manager.dt

        if keys[K_q]:
            self.rot += self.rot_speed * self.manager.dt
        if keys[K_e]:
            self.rot -= self.rot_speed * self.manager.dt

    def draw(self) -> None:
        self.manager.window.render(self.image, screen_pos(self, self.scene.camera))