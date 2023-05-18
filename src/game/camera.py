from src.management.scene import Scene
from src.game.player import Player
from src.common import *

class Camera:
    def __init__(self, scene: Scene, player: Player) -> None:
        self.manager = scene.manager
        self.scene = scene
        self.player = player
        self.pos = self.player.pos - HSIZE + self.player.size // 2

    def update(self) -> None:
        offset = self.player.pos - self.pos - HSIZE + self.player.size // 2
        self.pos += offset * 2 * self.manager.dt