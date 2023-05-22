from random import choice, randint
from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class StackedSprite(Sprite):
    def __init__(self, scene: Scene, layer: int | Layers, faces: list[pygame.SurfaceType], pos: tuple[int, int]) -> None:
        super().__init__(scene, layer)
        self.pos = VEC(pos)
        self.side_faces = faces[:-1]
        self.top_face = faces[-1]
        self.images = self.build_images()
        self.shader = Shader(self.manager.window, vert="res/shaders/stack.vert")

    def build_images(self) -> list[pygame.SurfaceType]:
        images = []

        r = RESOLUTION
        for i in range(15):
            images.append(surf := pygame.Surface((64, 64)))
            surf.blit(self.side_faces[0].subsurface((0, 64 - i * r - r, 64, r)), (0, 0))
            surf.blit(pygame.transform.rotate(self.side_faces[1].subsurface((0, 64 - i * r - r, 64, r)), 90), (0, 0))
            surf.blit(pygame.transform.rotate(self.side_faces[2].subsurface((0, 64 - i * r - r, 64, r)), 180), (0, 64 - r))
            surf.blit(pygame.transform.rotate(self.side_faces[3].subsurface((0, 64 - i * r - r, 64, r)), 270), (64 - r, 0))

        images.append(surf := choice(img.cobblestones).copy())
        surf.blit(choice(img.cracks), (0, 0), special_flags=BLEND_RGB_SUB)

        return images

    def build_layer(self, layer: int) -> None:
        StackedSpriteLayer(self.scene, self, layer)

    def update(self) -> None:
        self.shader.send("u_screenSize", SIZE)
        self.shader.send("u_targetSize", self.scene.player.size)
        self.shader.send("u_cameraPos", self.scene.player.camera.pos)
        self.shader.send("u_cameraRot", self.scene.player.camera.rot)
        self.shader.send("u_resolution", RESOLUTION)

class StackedSpriteLayer(Sprite):
    def __init__(self, scene: Scene, parent: StackedSprite, layer: int) -> None:
        super().__init__(scene, parent._layer)
        self.parent = parent
        self.layer = layer
        self.pos = self.parent.pos
        self.image = Texture(self.manager.window, self.parent.images[self.layer], self.parent.shader)

    def draw(self) -> None:
        self.parent.shader.send("u_layer", self.layer)
        self.manager.window.render(self.image, self.pos)