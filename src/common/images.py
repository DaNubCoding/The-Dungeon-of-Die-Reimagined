import pygame

from src.common.exe import pathof

def load_image(file: str, scale: int = 1) -> pygame.SurfaceType:
    return pygame.transform.scale_by(pygame.image.load(pathof(f"res/assets/textures/{file}")).convert_alpha(), scale)

pygame.display.set_mode((1, 1), pygame.NOFRAME)

cobblestone_spritesheet = load_image("cobblestone.png", 4)
cobblestones = [cobblestone_spritesheet.subsurface((0, i * 64, 64, 64)) for i in range(cobblestone_spritesheet.get_height() // 64)]

crack_spritesheet = load_image("crack.png", 4)
cracks = [crack_spritesheet.subsurface((0, i * 64, 64, 64)) for i in range(crack_spritesheet.get_height() // 64)]

pygame.display.quit()