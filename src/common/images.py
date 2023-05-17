import pygame

from src.common.exe import pathof

def load_image(file: str, scale: int = 1) -> pygame.SurfaceType:
    return pygame.transform.scale_by(pygame.image.load(pathof(f"res/assets/textures/{file}")).convert_alpha(), scale)

class SpriteSheet(list):
    def __init__(self, path: str, scale: int = 1, size: tuple[int, int] = (64, 64)) -> None:
        self.image = load_image(path, scale)
        for i in range(self.image.get_height() // size[1]):
            self.append(self.image.subsurface((0, i * size[1], *size)))

pygame.display.set_mode((1, 1), pygame.NOFRAME)

cobblestones = SpriteSheet("cobblestone.png", scale=4)
cracks = SpriteSheet("crack.png", scale=4)
for i in range(len(cracks)):
    cracks.append(pygame.transform.rotate(cracks[i], 90))
    cracks.append(pygame.transform.rotate(cracks[i], 180))
    cracks.append(pygame.transform.rotate(cracks[i], 270))

pygame.display.quit()