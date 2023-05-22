from random import randint, choice
from pygame.locals import *
import pygame

from src.game.stacked_sprite import StackedSprite
from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common import *

class TileManager:
    def __init__(self, scene: Scene) -> None:
        self.stacked_sprites: list[StackedSprite] = []
        for y in range(12):
            for x in range(16):
                if x == 0 or x == 15 or y == 0 or y == 11:
                    self.stacked_sprites.append(Wall(scene, (x * 64, y * 64)))
                else:
                    Ground(scene, (x * 64, y * 64))

        for i in range(16):
            for sprite in self.stacked_sprites:
                sprite.build_layer(i)

class Tile(StackedSprite):
    def __init__(self, scene: Scene, layer: int | Layers, faces: list[pygame.SurfaceType], pos: tuple[int, int]) -> None:
        self.side_faces = faces[:-1]
        self.top_face = faces[-1]
        self.images = self.build_images()
        super().__init__(scene, layer, self.images, pos)

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

class Ground(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, Layers.GROUND)
        image = choice(img.cobblestones).copy()
        if randint(0, 1):
            image.blit(choice(img.cracks), (0, 0))
        (trans_surf := pygame.Surface(image.get_size())).fill((15, 15, 15))
        image.blit(trans_surf, (0, 0), special_flags=BLEND_RGB_SUB)
        self.image = Texture(self.manager.window, image, self.scene.player.camera.shader)

        self.size = self.image.size
        self.pos = VEC(pos)

    def draw(self) -> None:
        self.manager.window.render(self.image, self.pos)

class Wall(Tile):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        faces: list[pygame.SurfaceType] = [choice(img.cobblestones).copy() for _ in range(5)]
        for face in faces:
            face.blit(choice(img.cracks), (0, 0), special_flags=BLEND_RGB_SUB)

        super().__init__(scene, Layers.WALL, faces, pos)