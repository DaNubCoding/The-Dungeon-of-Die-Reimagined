from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.level import Level

from random import randint, choice
from typing import Generator
from src.game.level.sprack_group import SprackGroup
from src.management.scene import Scene

class WallGroup(SprackGroup):
    def __init__(self, scene: Scene, level: Level) -> None:
        super().__init__(scene, level, "wall")
        self.obstructing = []

    def update(self) -> None:
        super().update()
        self.shader.send("u_playerPos", self.scene.player.center - self.pos)