from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.sprack import Sprack
from src.game.camera import Camera
from src.common import *

class Dice(Sprack):
    def __init__(self, scene: Scene) -> None:
        print("Loading player...")

        self.size = VEC(64, 64)
        self.pos = VEC(3, 6) * 64
        self.rot_speed = 1.8
        self.rot = 0

        super().__init__(scene, self.build_images(), self.pos)

        self.camera = Camera(self.scene, self)

    @property
    def center(self) -> tuple[int, int]:
        return self.pos + self.size // 2

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

        if K_w in self.manager.key_downs:
            self.roll(0)
        if K_d in self.manager.key_downs:
            self.roll(1)
        if K_s in self.manager.key_downs:
            self.roll(2)
        if K_a in self.manager.key_downs:
            self.roll(3)

        if keys[K_LEFT]:
            self.rot += self.rot_speed * self.manager.dt
        if keys[K_RIGHT]:
            self.rot -= self.rot_speed * self.manager.dt

        self.camera.update()

        super().update()

    def roll(self, direction: int) -> None:
        move = VEC(0, -64).rotate(direction * 90).rotate(-self.rot)
        if abs(move.x) > abs(move.y):
            move = VEC(sign(move.x) * 64, 0)
        else:
            move = VEC(0, sign(move.y) * 64)

        if inttup(self.pos // 64 + move.normalize()) in self.scene.level.wall_group.walls: return

        self.pos += move