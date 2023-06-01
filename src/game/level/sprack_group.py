from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.level import Level

from random import randint, choice
from typing import Generator
from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.sprack import Sprack
from src.common import *
from ._utils import *

class SprackGroup(Sprack):
    def __init__(self, scene: Scene, level: Level, frag_shader: str = "default") -> None:
        self.scene = scene
        self.level = level
        self.frag_shader = frag_shader
        self.spracks = []

        self.min_x = self.min_y = float("inf")
        self.max_x = self.max_y = self.height = 0
        self.pos = self.size = VEC(0, 0)

    def setup(self) -> None:
        images = [pygame.Surface(self.size, SRCALPHA) for _ in range(self.height)]
        for layer, image in enumerate(images):
            for sprack in self.spracks:
                image.blit(sprack.images[layer], sprack.pos - self.pos)

        for sprack in self.spracks:
            sprack.groupify()

        super().__init__(self.scene, images, self.pos, frag_shader=self.frag_shader)

    def __iter__(self) -> Generator:
        yield from self.spracks

    def add(self, sprack: Sprack) -> None:
        self.spracks.append(sprack)

        self.min_x = min(self.min_x, sprack.pos.x)
        self.max_x = max(self.max_x, sprack.pos.x)
        self.min_y = min(self.min_y, sprack.pos.y + sprack.size.x)
        self.max_y = max(self.max_y, sprack.pos.y + sprack.size.y)

        self.pos = VEC(self.min_x, self.min_y)
        self.size = VEC(self.max_x, self.max_y) - self.pos
        self.height = max(self.height, sprack.height)