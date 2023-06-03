from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.level import Level

from src.management.scene import Scene
from src.game.sprack import Sprack
from src.common import *
from ._utils import *

class Ground(Sprack):
    def __init__(self, scene: Scene, level: Level, pos: tuple[int, int]) -> None:
        self.level = level
        images = [darken(ground_texture(), 17)]
        super().__init__(scene, images, pos, self.level.ground_group)