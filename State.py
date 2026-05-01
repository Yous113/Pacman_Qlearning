from vector import Vector2
from constants import *

class State:
    def __init__(
            self, 
            playerPosition: Vector2, 
            nearestGhostDirection = None, 
            nearestGhostDistance = "none", 
            nearestpelletDirection = None, 
            isNearestGhostFreight = False
            ) -> None:
        
        self.playerPosition = playerPosition.asTuple()

        # Direction to the nearest ghost (Right, Left, Up, Down or None if no ghost is nearby)
        self.nearestGhostDirection = nearestGhostDirection

        self.nearestGhostDistance = nearestGhostDistance

        # Direction to the nearest pellet (Right, Left, Up, Down or None if no pellet is nearby)
        self.nearestpelletDirection = nearestpelletDirection

        # Boolean indicating if the nearest ghost is in freight mode
        self.isNearestGhostFreight = isNearestGhostFreight

    def __str__(self):
        return "{}.{}.{}.{}.{}.{}".format(
            self.playerPosition[0],
            self.playerPosition[1],
            self.nearestGhostDirection,
            self.nearestGhostDistance,
            self.nearestpelletDirection,
            self.isNearestGhostFreight
        )

        