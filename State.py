from vector import Vector2
from constants import *


"""
    State representation for the Q-learning algorithm. 
    The state is represented as a string, which is used as a key in the Q-table. 
    The state includes the tile position of the player, the direction and distance to the nearest ghost, 
    the direction to the nearest pellet and whether the nearest ghost is in freight mode. 
    This representation allows the Q-learning algorithm to learn from the environment and make informed decisions based on the current state of the game.
"""
class State:
    def __init__(
            self, 
            playerPosition: Vector2, 
            nearestGhostDirection = None, 
            nearestGhostDistance = "none", 
            nearestpelletDirection = None, 
            isNearestGhostFreight = False
            ) -> None:
        # tileposition keeps the qtable smaller and is enough to represent the state, we don't need the exact pixel position
        self.playerPosition = (
            int(playerPosition.x / TILEWIDTH), 
            int(playerPosition.y / TILEHEIGHT)
            )

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

        