from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.game.camera import Camera
from src.common import *

class Player(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.PLAYER)
        self.size = VEC(48, 48)
        self.pos = VEC(64, 64)
        self.vel = VEC(0, 0)
        self.speed = 3
        self.rot_speed = 1
        self.rot = 0

        self.camera = Camera(self.scene, self)
        self.image = pygame.Surface(self.size, SRCALPHA)
        self.image.fill((255, 0, 0))
        self.image = Texture(self.manager.window, self.image, self.camera.shader)

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
        self.vel.rotate_ip(-self.rot)

        if keys[K_LEFT]:
            self.rot += self.rot_speed * self.manager.dt
        if keys[K_RIGHT]:
            self.rot -= self.rot_speed * self.manager.dt

        self.pos.x += floor(self.vel.x) * self.manager.dt
        self.rect = pygame.Rect(self.pos, self.size)
        for tile in self.scene.tile_manager.walls:
            if not tile.rect.colliderect(self.rect): continue
            if self.vel.x < 0:
                self.pos.x = tile.rect.right
            elif self.vel.x > 0:
                self.pos.x = tile.rect.left - self.size.x

        self.pos.y += floor(self.vel.y) * self.manager.dt
        self.rect = pygame.Rect(self.pos, self.size)
        for tile in self.scene.tile_manager.walls:
            if not tile.rect.colliderect(self.rect): continue
            if self.vel.y < 0:
                self.pos.y = tile.rect.bottom
            elif self.vel.y > 0:
                self.pos.y = tile.rect.top - self.size.y

        self.camera.update()

    def draw(self) -> None:
        self.manager.window.render(self.image, self.pos)