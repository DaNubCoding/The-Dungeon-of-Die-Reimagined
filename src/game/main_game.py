from src.game.level.level import Level
from src.management.scene import Scene
from src.game.dice import Dice
from src.common import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.spracks = []
        self.player = Dice(self)
        self.level = Level(self, 1)
        for sprack in self.spracks:
            print(sprack.__class__.__name__)

        for i in range(128 // RESOLUTION):
            for sprite in self.spracks:
                sprite.build_layer(i)

    def update(self) -> None:
        super().update()

    def draw(self) -> None:
        self.manager.window.fill((0, 0, 0))
        super().draw()