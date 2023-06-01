from src.game.level.sprack_group import SprackGroup
from src.game.level.wall_group import WallGroup
from src.game.level.ground import Ground
from src.management.scene import Scene
from src.game.level.wall import Wall
from src.common import *
from ._utils import *

class Level:
    def __init__(self, scene: Scene, level: int) -> None:
        self.scene = scene
        self.level_num = level
        self.load()

        self.ground_group = SprackGroup(self.scene, self)
        self.wall_group = WallGroup(self.scene, self)

        for pos in self.ground_positions:
            Ground(self.scene, self, VEC(pos) * 64)
        self.ground_group.setup()

        for pos in self.wall_positions:
            Wall(self.scene, self, pos, exposed_sides(pos, self.wall_positions))
        self.wall_group.setup()

    def load(self) -> None:
        self.ground_positions, self.wall_positions = set(), set()
        _file = open(f"res/levels/{self.level_num}.txt", "r")

        y = 0
        while line := _file.readline().removesuffix("\n"):
            for x, ch in enumerate(line):
                if ch == " ": continue
                self.ground_positions.add((x, y))
                if ch != "#": continue
                self.wall_positions.add((x, y))
            y += 1

        _file.close()