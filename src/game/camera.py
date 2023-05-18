from src.management.scene import Scene
from src.game.player import Player
from src.common import *

class Camera:
    def __init__(self, scene: Scene, player: Player) -> None:
        self.manager = scene.manager
        self.scene = scene
        self.player = player
        self.pos = self.player.pos.copy()
        self.rot = self.player.rot

    def update(self) -> None:
        offset = self.player.pos - self.pos
        offset = snap(offset, VEC(), VEC(1, 1))
        self.pos += offset * 5 * self.manager.dt

        rot_offset = self.player.rot - self.rot
        rot_offset = snap(rot_offset, 0, 1)
        self.rot += rot_offset * 5 * self.manager.dt