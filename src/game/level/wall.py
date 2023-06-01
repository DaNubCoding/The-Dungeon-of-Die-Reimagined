from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.level import Level

import pygame

from src.management.scene import Scene
from src.game.sprack import Sprack
from src.common import *
from ._utils import *

class Wall(Sprack):
    def __init__(self, scene: Scene, level: Level, pos: tuple[int, int], exposed: list[bool]) -> None:
        self.level = level

        self.exposed = exposed
        *self.side_faces, self.top_face = [cobblestone_texture() for _ in range(9)]

        super().__init__(scene, self.build_images(), VEC(pos) * 64, self.level.wall_group)
        self.screen_pos = self.pos.copy()
        self.rect = pygame.Rect(*self.pos, 64, 64)

    def build_images(self) -> list[pygame.SurfaceType]:
        images = [generate_layer(self.side_faces[:4], layer, self.exposed) for layer in range(64 // RESOLUTION)]
        images += [generate_layer(self.side_faces[4:], layer, self.exposed) for layer in range(64 // RESOLUTION - 1)]
        images.append(self.top_face)
        return images

    def update(self) -> None:
        super().update()
        self.screen_pos = (self.pos - self.scene.player.camera.pos).rotate(self.scene.player.camera.rot) + VEC(SIZE) // 2
        if HEIGHT // 2 + 10 < self.screen_pos.y < HEIGHT // 2 + 180 and WIDTH // 2 - 100 < self.screen_pos.x < WIDTH // 2 + 100:
            self.group.obstructing.append(self.pos - self.group.pos)