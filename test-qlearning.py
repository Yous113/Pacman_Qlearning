from qLearningController import QlearningController
from State import State
from vector import Vector2
from constants import UP, DOWN, LEFT, RIGHT


controller = QlearningController()

oldState = State(Vector2(100, 100))
newState = State(Vector2(116, 100))

action = RIGHT
newActions = [UP, DOWN, LEFT, RIGHT]

print("Before:", controller.qTable.getQvalue(oldState, action))

controller.updateQvalue(
    oldState,
    action,
    reward=10,
    newState=newState,
    newActions=newActions
)

print("After:", controller.qTable.getQvalue(oldState, action))