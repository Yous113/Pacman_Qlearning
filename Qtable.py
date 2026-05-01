import os
import pickle


class Qtable:
    def __init__(self, filename="qtable.txt"):
        self.qTable = {}
        self.filename = filename

    def makeKey(self, state, action):
        # The teacher guide says we need a hash/key for the state-action pair.
        # We combine state and action into one string.
        return str(state) + "." + str(action)

    def storeQvalue(self, state, action, value):
        key = self.makeKey(state, action)
        self.qTable[key] = value

    def getQvalue(self, state, action):
        key = self.makeKey(state, action)
        return self.qTable.get(key, 0.0)

    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.qTable, file)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as file:
                self.qTable = pickle.load(file)
        else:
            self.save()