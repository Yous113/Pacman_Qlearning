from vector import Vector2
from constants import *

class State:
    def __init__(self, playerPosition: Vector2, nearestGhostDirection = None, nearestGhostDistance = "none") -> None:
        self.playerPosition = playerPosition.asTuple()

        # Direction to the nearest ghost (Right, Left, Up, Down or None if no ghost is nearby)
        self.nearestGhostDirection = nearestGhostDirection

        self.nearestGhostDistance = nearestGhostDistance

    def __str__(self):
        return "{}.{}.{}.{}".format(
            self.playerPosition[0],
            self.playerPosition[1],
            self.nearestGhostDirection,
            self.nearestGhostDistance
        )

        