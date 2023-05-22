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
        self.connected: list[set] = []

        _file = open("res/levels/1.txt", "r")
        y = 0
        while line := _file.readline():
            for x, ch in enumerate(line):
                if ch == ".":
                    Ground(scene, (x * 64, y * 64))
                if ch != "#": continue
                for chunk in self.connected:
                    if (x - 1, y) in chunk: break
                    if (x, y - 1) in chunk: break
                else:
                    self.connected.append({(x, y)})
                    continue
                chunk.add((x, y))
            y += 1
        _file.close()

        for chunk in self.connected:
            self.stacked_sprites.append(WallGroup(scene, list(chunk)))

        for i in range(16):
            for sprite in self.stacked_sprites:
                sprite.build_layer(i)

class Wall:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = VEC(pos) * 64
        self.faces: list[pygame.SurfaceType] = [choice(img.cobblestones).copy() for _ in range(5)]
        for face in self.faces:
            face.blit(choice(img.cracks), (0, 0), special_flags=BLEND_RGB_SUB)
        self.side_faces = self.faces[:-1]
        self.top_face = self.faces[-1]
        self.images = self.build_images()

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

class WallGroup(StackedSprite):
    def __init__(self, scene: Scene, positions: list[tuple[int, int]]) -> None:
        corner1 = VEC(min(pos[0] for pos in positions) * 64, min(pos[1] for pos in positions) * 64)
        corner2 = VEC(max(pos[0] for pos in positions) * 64 + 64, max(pos[1] for pos in positions) * 64 + 64)
        images = [pygame.Surface(corner2 - corner1, SRCALPHA) for _ in range(64 // RESOLUTION)]
        walls = [Wall(pos) for pos in positions]
        for layer, image in enumerate(images):
            for wall in walls:
                image.blit(wall.images[layer], wall.pos - corner1)
        super().__init__(scene, Layers.WALL, images, corner1)

class Ground(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, Layers.GROUND)
        image = choice(img.cobblestones).copy()
        if randint(0, 1):
            image.blit(choice(img.cracks), (0, 0))
        (trans_surf := pygame.Surface(image.get_size())).fill((17, 17, 17))
        image.blit(trans_surf, (0, 0), special_flags=BLEND_RGB_SUB)
        self.image = Texture(self.manager.window, image, self.scene.player.camera.shader)

        self.size = self.image.size
        self.pos = VEC(pos)

    def draw(self) -> None:
        self.manager.window.render(self.image, self.pos)