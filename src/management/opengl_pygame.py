from __future__ import annotations

from pygame.math import Vector2 as VEC
from typing import Optional
from pygame.locals import *
import moderngl
import struct
import pygame
import os

DEFAULT_VERT = "res/shaders/default.vert"
DEFAULT_FRAG = "res/shaders/default.frag"

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it."""
    with open(path, "r") as file:
        return file.read()

class Window:
    """Wrapper for Pygame window and ModernGL context."""
    def __init__(self, width: int, height: int) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "200,200"
        self.width, self.height = self.size = width, height
        pygame.init()
        self.display = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | OPENGL)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.uvmap = self.ctx.buffer(struct.pack("8f", *[0, 1, 1, 1, 0, 0, 1, 0]))
        self.ibo = self.ctx.buffer(struct.pack("6I", *[0, 1, 2, 1, 2, 3]))

    def render(self, surface: Texture, pos: tuple[int, int]) -> None:
        """Render a surface onto the window default framebuffer."""
        self.ctx.screen.use()
        surface.texture.use()
        surface.shader.send("u_texSize", surface.size)
        surface.move(pos)
        surface.vao.render()

    def fill(self, color: tuple[int, int, int]) -> None:
        """Fill the default framebuffer with the specified color."""
        self.ctx.screen.use()
        self.ctx.clear(color[0] / 255, color[1] / 255, color[2] / 255)

    def rect_vertices(self, size: tuple[int, int]) -> list[int]:
        """Return the normalized coordinates of the vertices of a rect based on the size of the window, it will be at position 0"""
        size = size[0] / self.width * 2, size[1] / self.height * 2
        return [
            0       - 1, 0        + 1,
            size[0] - 1, 0        + 1,
            0       - 1, -size[1] + 1,
            size[0] - 1, -size[1] + 1,
        ]

class Shader:
    """Wrapper for a ModernGL shader program."""
    def __init__(self, window: Window, frag=DEFAULT_FRAG, vert=DEFAULT_VERT) -> None:
        self.window = window
        self.vert = read_file(vert)
        self.frag = read_file(frag)
        self.program = window.ctx.program(vertex_shader=self.vert, fragment_shader=self.frag)

    def send(self, name: str, value: float | tuple[float, float]) -> None:
        """Send a uniform variable to the shader."""
        try:
            self.program[name].value = value if isinstance(value, (float, int)) else tuple(value)
        except KeyError:
            pass

    def get(self, name: str) -> float | tuple[float, float]:
        """Get the value of a uniform variable previously sent to the shader."""
        return self.program[name].value

    def move(self, pos: tuple[int, int]) -> None:
        """Prepare the shader to render with an offset next time"""
        self.send("u_position", pos)
        self.send("u_screenSize", self.window.size)

class Texture:
    def __init__(self, window: Window, src: pygame.Surface | str, shader: Optional[Shader] = None) -> None:
        self.window = window
        self.shader = shader if shader is not None else Shader(window)
        self.ctx = window.ctx
        if isinstance(src, str):
            src = pygame.image.load(src).convert_alpha()
        self.surf = src.convert_alpha()

        self.texture = self.ctx.texture(self.surf.get_size(), 4, pygame.transform.flip(self.surf, False, True).get_view())
        self.texture.repeat_x, self.texture.repeat_y, self.texture.swizzle = False, False, "BGRA"
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.size = size = VEC(self.surf.get_size())

        self.vbo = self.ctx.buffer(struct.pack("8f", *self.window.rect_vertices(size)))
        self.vao_content = [(self.vbo, "2f", "vertexPos"), (self.window.uvmap, "2f", "vertexTexCoord")]
        self.vao = self.ctx.vertex_array(self.shader.program, self.vao_content, self.window.ibo)

    def move(self, pos: tuple[int, int]) -> None:
        self.shader.move(pos)