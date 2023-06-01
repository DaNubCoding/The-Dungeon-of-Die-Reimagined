from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.level.sprack_group import SprackGroup

from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class Sprack(Sprite):
    def __init__(self, scene: Scene, images: list[pygame.SurfaceType], pos: tuple[int, int], group: SprackGroup = None, frag_shader: str = "default") -> None:
        super().__init__(scene, Layers.SPRACKS)
        self.scene.spracks.append(self)
        self.group = group
        self.pos = VEC(pos)
        self.images = images
        self.size = VEC(self.images[0].get_size())
        self.height = len(self.images)
        self.layers: list[SprackLayer] = []

        self.shader = Shader(self.manager.window, f"res/shaders/{frag_shader}.frag", "res/shaders/sprack.vert")

        if self.group:
            self.group.add(self)

    def build_layer(self, layer: int) -> None:
        if layer >= len(self.images): return
        self.layers.append(SprackLayer(self.scene, self, layer))

    def update(self) -> None:
        self.shader.send("u_screenSize", SIZE)
        self.shader.send("u_targetSize", self.scene.player.size)
        self.shader.send("u_cameraPos", self.scene.player.camera.pos)
        self.shader.send("u_cameraRot", self.scene.player.camera.rot)
        self.shader.send("u_cameraScale", self.scene.player.camera.scale)
        self.shader.send("u_resolution", RESOLUTION)

    def groupify(self) -> None:
        for layer in self.layers:
            layer.kill()
        self.scene.spracks.remove(self)
        self.shader.release()

class SprackLayer(Sprite):
    def __init__(self, scene: Scene, parent: Sprack, layer: int) -> None:
        super().__init__(scene, Layers.SPRACKS)
        self.parent = parent
        self.layer = layer
        self.pos = self.parent.pos
        self.image = Texture(self.manager.window, self.parent.images[self.layer], self.parent.shader)

    def draw(self) -> None:
        self.parent.shader.send("u_layer", self.layer)
        self.manager.window.render(self.image, self.pos)