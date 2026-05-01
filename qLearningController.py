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

        self.learnCounter = 0

        # Used to avoid saving the Q-table every frame
        self.saveCounter = 0

    def setTrainingMode(self, training):
        if training:
            self.rho = 0.5
        else:
            self.rho = 0.1


    def learn(self, game):
        # To prevent error on the first update, we wait until we have a previous state and action to learn from
        if self.previousState is None or self.previousAction is None:
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

        self.learnCounter += 1

        # occasionally print out some information about the learning progress
        if self.learnCounter % 300 == 0:
            print("Score:", game.score, "Lives:", game.lives, "Q-table size:", len(self.qTable.qTable))

    def getAction(self, state, actions):
        if len(actions) == 0:
            return STOP
        
        # Exploration - choose a random action
        if random.random() < self.rho:
            action = random.choice(actions)
        else: 
            # Exploitation - choose the action with the highest Q-value
            bestQValue = None
            bestActions = []
            

            for possibleAction  in actions:
                qVal = self.qTable.getQvalue(state, possibleAction)

                if bestQValue is None or qVal > bestQValue:
                    bestQValue = qVal
                    bestActions = [possibleAction]
                elif qVal == bestQValue:
                    bestActions.append(possibleAction)
            
            # if there are multiple best actions, choose randomly among them
            action = random.choice(bestActions)

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
        self.saveCounter += 1
        # occasionally save the Q-table to a file avoid save every frame
        if self.saveCounter % 300 == 0:
            self.qTable.save()

    def getState(self, game):
        pacman = game.pacman
        nearestGhost = self.getNearestGhost(pacman, game.ghosts)

        nearestGhostDirection = self.getNearestGhostDirection(pacman, nearestGhost)
        nearestGhostDistance = self.nearestGhostDistance(pacman, nearestGhost)
        nearestpelletDirection = self.getNearestPelletDirection(pacman, game.pellets.pelletList)

        nearestGhostFreight = False
        if nearestGhost is not None:
            nearestGhostFreight = nearestGhost.mode.current == FREIGHT

        state = State(pacman.position, nearestGhostDirection, nearestGhostDistance, nearestpelletDirection, nearestGhostFreight)
    
        return state
    
    def getNearestGhost(self, pacman, ghosts):
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
        
        return nearestGhost
    
    def getNearestPelletDirection(self, pacman, pellets):
        nearestPellet = None
        nearestDistance = None

        for pellet in pellets:
            difference = pellet.position - pacman.position
            distance = difference.magnitudeSquared()

            if nearestDistance is None or distance < nearestDistance:
                nearestPellet = pellet
                nearestDistance = distance
        
        # None = no pellets
        if nearestPellet is None:
            return None
        
        difference = nearestPellet.position - pacman.position

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
            
    # simple heuristic to get the distance of the nearest ghost, used as part of the state
    def nearestGhostDistance(self, pacman, ghost):
        if ghost is None:
            return "none"
        
        difference = ghost.position - pacman.position
        distance = difference.magnitudeSquared()

        closeLimit = (TILEWIDTH * 5) ** 2
        mediumLimit = (TILEWIDTH * 10) ** 2

        if distance <= closeLimit:
            return "close"
        elif distance <= mediumLimit:
            return "medium"
        else:
            return "far"

    # simple heuristic to get the direction of the nearest ghost, used as part of the state
    def getNearestGhostDirection(self, pacman, ghost):
        # None = no ghosts
        if ghost is None:
            return None
        
        difference = ghost.position - pacman.position

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
        # pellet + 10, power pellet +50, fruit +100, ghost eaten +200
        reward = game.score - self.previousScore

        # death is bad, give a large negative reward
        if game.lives < self.previousLives or not game.pacman.alive:
            reward -= 500

        # penalty for reversing direction, to encourage smoother movement
        if self.previousAction == game.pacman.direction * -1:
            reward -= 3

        # nothing useful happened, give a small negative reward to encourage learning
        if reward == 0:
            reward -= 1

        return reward    

        
