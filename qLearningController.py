from Qtable import Qtable
import random
from constants import *

from State import State

class QlearningController:
    def __init__(self):
        # Q-table: key: state, value: q-values
        self.qTable = Qtable()
        self.qTable.load()

        # state and action from the previous update, used for learning
        self.previousState = None
        self.previousAction = None

        # used to calculate reward
        self.previousScore = 0
        self.previousLives = 5

        # Learning rate
        self.alpha = 0.1
        
        # Discount rate
        self.gamma = 0.9

        # Exploration rate
        self.rho = 0.1


    def learn(self, game):
        # To prevent error on the first update, we wait until we have a previous state and action to learn from
        if self.previousState is None and self.previousAction is None:
            self.previousScore = game.score
            self.previousLives = game.lives
            return
        
        reward = self.calculateReward(game)

        newState = self.getState(game)
        newActions = self.getActions(game.pacman)

        self.updateQvalue(
            self.previousState,
            self.previousAction,
            reward,
            newState,
            newActions
        )

        self.previousScore = game.score
        self.previousLives = game.lives

    def getAction(self, state, actions):
        if len(actions) == 0:
            return STOP
        
        # Exploration - choose a random action
        if random.random() < self.rho:
            action = random.choice(actions)
        else: 
            # Exploitation - choose the action with the highest Q-value
            bestAction = actions[0]
            bestQValue = self.qTable.getQvalue(state, bestAction)

            for possibleAction  in actions:
                qVal = self.qTable.getQvalue(state, possibleAction)

                if qVal > bestQValue:
                    bestQValue = qVal
                    bestAction = possibleAction
            
            action = bestAction

        self.previousAction = action
        self.previousState = state

        return action


    def updateQvalue(self, state, action, reward, newState, newActions):
        oldQValue = self.qTable.getQvalue(state, action)

        # If there are no new actions, we cant calculate future Q-value, so we just use the reward.
        if len(newActions) == 0:
            maxFutureQValue = 0.0
        else:
            # Get the maximum Q-value for the new state across all possible actions
            # Q(s, a) = (1-α)Q(s, a) + α(r + γMax(Q(s’, a’))) 
            maxFutureQValue = max([self.qTable.getQvalue(newState, newAction) for newAction in newActions])

        newQValue = (1 - self.alpha) * oldQValue + self.alpha * (reward + self.gamma * maxFutureQValue)

        self.qTable.storeQvalue(state, action, newQValue)
        self.qTable.save()

    def getState(self, game):
        pacman = game.pacman
        nearestGhostDirection = self.getNearestGhostDirection(pacman, pacman.game.ghosts)
        nearestGhostDistance = self.nearestGhostDistance(pacman, pacman.game.ghosts)

        return State(pacman.position, nearestGhostDirection, nearestGhostDistance)

    # simple heuristic to get the distance of the nearest ghost, used as part of the state
    def nearestGhostDistance(self, pacman, ghosts):
        nearestDistance = None

        for ghost in ghosts:
            if not ghost.visible:
                continue

            difference = ghost.position - pacman.position
            distance = difference.magnitudeSquared()

            if nearestDistance is None or distance < nearestDistance:
                nearestDistance = distance

        if nearestDistance is None:
            return "none"

        closeLimit = (TILEWIDTH * 5) ** 2
        mediumLimit = (TILEWIDTH * 10) ** 2

        if nearestDistance <= closeLimit:
            return "close"
        elif nearestDistance <= mediumLimit:
            return "medium"
        else:
            return "far"

    # simple heuristic to get the direction of the nearest ghost, used as part of the state
    def getNearestGhostDirection(self, pacman, ghosts):
        nearestGhost = None
        nearestDistance = None

        for ghost in ghosts:
            if not ghost.visible:
                continue    

            difference = ghost.position - pacman.position
            distance = difference.magnitudeSquared()

            if nearestDistance is None or distance < nearestDistance:
                nearestGhost = ghost
                nearestDistance = distance
        
        # None = no ghosts
        if nearestGhost is None:
            return None
        
        difference = nearestGhost.position - pacman.position

        if abs(difference.x) > abs(difference.y):
            if difference.x > 0:
                return RIGHT
            else:
                return LEFT
        else:
            if difference.y > 0:
                return DOWN
            else:
                return UP
    
    def getActions(self, pacman):
        return pacman.validDirections()
    
    def calculateReward(self, game):
        
        # If score is increased, give a positive reward
        reward = game.score - self.previousScore

        # death is bad, give a large negative reward
        if game.lives < self.previousLives or not game.pacman.alive:
            reward -= 500

        # nothing useful happened, give a small negative reward to encourage learning
        if reward == 0:
            reward -= 1

        return reward    

        
