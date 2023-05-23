from random import randint, choice
from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.game.sprack import Sprack
from src.common import *

class TileManager:
    def __init__(self, scene: Scene) -> None:
        self.spracks: list[Sprack] = []
        self.walls: set[tuple[int, int]] = set()

        _file = open("res/levels/1.txt", "r")
        y = 0
        while line := _file.readline():
            for x, ch in enumerate(line):
                if ch == ".":
                    Ground(scene, (x * 64, y * 64))
                if ch != "#": continue
                self.walls.add((x, y))
            y += 1
        _file.close()

        self.spracks.append(WallGroup(scene, self.walls))

        for i in range(64 // RESOLUTION):
            for sprite in self.spracks:
                sprite.build_layer(i)

class Wall:
    def __init__(self, pos: tuple[int, int], exposed_sides: list[bool]) -> None:
        self.pos = VEC(pos) * 64
        self.exposed_sides = exposed_sides
        self.faces: list[pygame.SurfaceType] = [choice(img.cobblestones).copy() for _ in range(5)]
        for face in self.faces:
            face.blit(choice(img.cracks), (0, 0), special_flags=BLEND_RGB_SUB)
        self.side_faces = self.faces[:-1]
        self.top_face = self.faces[-1]
        self.images = self.build_images()

    def build_images(self) -> list[pygame.SurfaceType]:
        images = []

        for layer in range(64 // RESOLUTION - 1):
            images.append(surf := pygame.Surface((64, 64), SRCALPHA))
            for i, exposed in enumerate(self.exposed_sides):
                if exposed: continue
                self.draw_edge(surf, i, layer)
            for i, exposed in enumerate(self.exposed_sides):
                if not exposed: continue
                self.draw_edge(surf, i, layer)

        images.append(surf := choice(img.cobblestones).copy())
        surf.blit(choice(img.cracks), (0, 0), special_flags=BLEND_RGB_SUB)

        return images

    def draw_edge(self, surf: pygame.SurfaceType, edge: int, layer: int) -> None:
        edge_surf = self.side_faces[edge].subsurface((0, 64 - layer * RESOLUTION - RESOLUTION, 64, RESOLUTION))
        (trans_surf := pygame.Surface(edge_surf.get_size())).fill(((edge % 2 + 1) * 4 + (64 // RESOLUTION - layer) * 0.1, ) * 3)
        edge_surf.blit(trans_surf, (0, 0), special_flags=BLEND_RGB_SUB)
        edge_surf = pygame.transform.scale(edge_surf, (edge_surf.get_width(), RESOLUTION + 1))
        surf.blit(pygame.transform.rotate(edge_surf, 90 * edge), [(0, 0), (0, 0), (0, 64 - RESOLUTION - 1), (64 - RESOLUTION - 1, 0)][edge])

class WallGroup(Sprack):
    def __init__(self, scene: Scene, positions: set[tuple[int, int]]) -> None:
        corner1 = VEC(min(pos[0] for pos in positions) * 64, min(pos[1] for pos in positions) * 64)
        corner2 = VEC(max(pos[0] for pos in positions) * 64 + 64, max(pos[1] for pos in positions) * 64 + 64)
        images = [pygame.Surface(corner2 - corner1, SRCALPHA) for _ in range(64 // RESOLUTION)]

        walls = []
        for pos in positions:
            exposed = [
                (pos[0], pos[1] - 1) not in positions,
                (pos[0] - 1, pos[1]) not in positions,
                (pos[0], pos[1] + 1) not in positions,
                (pos[0] + 1, pos[1]) not in positions,
            ]
            walls.append(Wall(pos, exposed))

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