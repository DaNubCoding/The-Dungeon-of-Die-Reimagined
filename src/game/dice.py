from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.sprack import Sprack
from src.game.camera import Camera
from src.common import *

class Dice(Sprack):
    def __init__(self, scene: Scene) -> None:
        self.size = VEC(64, 64)
        self.pos = VEC(3, 6) * 64
        self.vel = VEC(0, 0)
        self.speed = 3
        self.rot_speed = 1.8
        self.rot = 0

        super().__init__(scene, self.build_images(), self.pos)

        self.camera = Camera(self.scene, self)

    def build_images(self) -> list[pygame.SurfaceType]:
        images = []

        for layer in range(64 // RESOLUTION - 1):
            images.append(surf := pygame.Surface(self.size, SRCALPHA))
            surf.blit(pygame.transform.scale(img.dice[0].subsurface((0, layer * RESOLUTION, 64, RESOLUTION)), (64, RESOLUTION + 1)), (0, 0))
            surf.blit(pygame.transform.scale(img.dice[5].subsurface((0, layer * RESOLUTION, 64, RESOLUTION)), (64, RESOLUTION + 1)), (0, 64 - RESOLUTION - 1))
            surf.blit(pygame.transform.rotate(pygame.transform.scale(img.dice[1].subsurface((0, layer * RESOLUTION, 64, RESOLUTION)), (64, RESOLUTION + 1)), 90), (0, 0))
            surf.blit(pygame.transform.rotate(pygame.transform.scale(img.dice[4].subsurface((0, layer * RESOLUTION, 64, RESOLUTION)), (64, RESOLUTION + 1)), 90), (64 - RESOLUTION - 1, 0))

        images.append(surf := pygame.Surface(self.size, SRCALPHA))
        surf.blit(img.dice[2], (0, 0))

        return images

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

        self.pos.x += self.vel.x * self.manager.dt
        self.rect = pygame.Rect(self.pos, self.size)
        for tile in self.scene.level.wall_group:
            if not tile.rect.colliderect(self.rect): continue
            if self.vel.x < 0:
                self.pos.x = tile.rect.right
            elif self.vel.x > 0:
                self.pos.x = tile.rect.left - self.size.x

        self.pos.y += self.vel.y * self.manager.dt
        self.rect = pygame.Rect(self.pos, self.size)
        for tile in self.scene.level.wall_group:
            if not tile.rect.colliderect(self.rect): continue
            if self.vel.y < 0:
                self.pos.y = tile.rect.bottom
            elif self.vel.y > 0:
                self.pos.y = tile.rect.top - self.size.y

        self.camera.update()

        super().update()