from src.management.scene import Scene
from src.game.tile import TileManager
from src.game.player import Player
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.spracks = []
        self.player = Player(self)
        self.tile_manager = TileManager(self)

        for i in range(64 // RESOLUTION):
            for sprite in self.spracks:
                sprite.build_layer(i)

    def update(self) -> None:
        super().update()

    def draw(self) -> None:
        self.manager.window.fill((0, 0, 0))
        super().draw()