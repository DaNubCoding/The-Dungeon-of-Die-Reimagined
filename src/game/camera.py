from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.player import Player

from src.management.scene import Scene
from src.common import *

class Camera:
    def __init__(self, scene: Scene, player: Player) -> None:
        self.manager = scene.manager
        self.scene = scene
        self.player = player
        self.pos = self.player.pos.copy()
        self.rot = self.player.rot
        self.shader = Shader(self.manager.window, vert="res/shaders/camera.vert")

    def update(self) -> None:
        offset = self.player.pos - self.pos
        offset = snap(offset, VEC(), VEC(1, 1))
        self.pos += offset * 0.15 * self.manager.dt

        rot_offset = self.player.rot - self.rot
        rot_offset = snap(rot_offset, 0, 1)
        self.rot += rot_offset * 0.15 * self.manager.dt

        self.shader.send("u_screenSize", SIZE)
        self.shader.send("u_targetSize", self.player.size)
        self.shader.send("u_cameraPos", self.pos)
        self.shader.send("u_cameraRot", self.rot)