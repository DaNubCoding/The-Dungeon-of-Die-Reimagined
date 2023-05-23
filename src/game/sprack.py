from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class Sprack(Sprite):
    def __init__(self, scene: Scene, layer: int | Layers, images: list[pygame.SurfaceType], pos: tuple[int, int]) -> None:
        super().__init__(scene, layer)
        self.pos = VEC(pos)
        self.shader = Shader(self.manager.window, vert="res/shaders/sprack.vert")
        self.images = images
        self.layers = []

    def build_layer(self, layer: int) -> None:
        self.layers.append(SprackLayer(self.scene, self, layer))

    def update(self) -> None:
        self.shader.send("u_screenSize", SIZE)
        self.shader.send("u_targetSize", self.scene.player.size)
        self.shader.send("u_cameraPos", self.scene.player.camera.pos)
        self.shader.send("u_cameraRot", self.scene.player.camera.rot)
        self.shader.send("u_cameraScale", self.scene.player.camera.scale)
        self.shader.send("u_resolution", RESOLUTION)

class SprackLayer(Sprite):
    def __init__(self, scene: Scene, parent: Sprack, layer: int) -> None:
        super().__init__(scene, parent._layer)
        self.parent = parent
        self.layer = layer
        self.pos = self.parent.pos
        self.image = Texture(self.manager.window, self.parent.images[self.layer], self.parent.shader)

    def draw(self) -> None:
        self.parent.shader.send("u_layer", self.layer)
        self.manager.window.render(self.image, self.pos)