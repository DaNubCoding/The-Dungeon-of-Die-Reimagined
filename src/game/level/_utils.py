from random import choice, randint
import pygame

from src.common import *

def cobblestone_texture() -> pygame.SurfaceType:
    image = choice(img.cobblestones).copy()
    if randint(0, 1):
        image.blit(choice(img.cracks), (0, 0), special_flags=pygame.BLEND_RGB_SUB)
    return image

def exposed_sides(pos: tuple[int, int], positions: set[tuple[int, int]]) -> list[bool]:
    return [
        (pos[0], pos[1] - 1) not in positions,
        (pos[0] - 1, pos[1]) not in positions,
        (pos[0], pos[1] + 1) not in positions,
        (pos[0] + 1, pos[1]) not in positions,
    ]

_side_positions = [(0, 0), (0, 0), (0, 64 - RESOLUTION - 1), (64 - RESOLUTION - 1, 0)]
def generate_layer(images: list[pygame.SurfaceType], layer: int, exposed: list[bool]) -> pygame.SurfaceType:
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    for i, image in enumerate(images):
        if not exposed[i]: continue
        _draw_side(surf, image, i, layer)
    return surf

def _draw_side(surf: pygame.SurfaceType, image: pygame.SurfaceType, edge_num: int, layer: int) -> None:
    edge_surf = image.subsurface((0, 64 - layer * RESOLUTION - RESOLUTION, 64, RESOLUTION))
    edge_surf = pygame.transform.scale(edge_surf, (edge_surf.get_width(), RESOLUTION + 1))
    surf.blit(pygame.transform.rotate(edge_surf, 90 * edge_num), _side_positions[edge_num])