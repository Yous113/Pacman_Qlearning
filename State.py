
import sys
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), '..'))

from vector import Vector2


class State:
    def __init__(self, playerPosition: Vector2) -> None:
        self.playerPosition = playerPosition.asTuple()

    def __str__(self):
        return "{}.{}".format(self.playerPosition[0], self.playerPosition[1])

        