from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.level import Level

from math import radians

from src.game.level.sprack_group import SprackGroup
from src.management.scene import Scene
from src.common import *

class WallGroup(SprackGroup):
    def __init__(self, scene: Scene, level: Level) -> None:
        super().__init__(scene, level, "wall")
        self.walls = {}

    def setup(self) -> None:
        super().setup()
        self.walls = {inttup(wall.pos // 64): wall for wall in self.spracks}

    def update(self) -> None:
        super().update()
        self.shader.send("u_playerPos", self.scene.player.center - self.pos + VEC(0, 75).rotate(-self.scene.player.rot))
        self.shader.send("u_playerRot", radians(self.scene.player.rot))