import re
from Board import Board

moveRegex = r'\s?\d+\.\s'

class Game:
    properties = {}
    gameStates = []
    moves = []

    def setProperty(self, property, value):
        self.properties[property] = value

    def simulateGame(self, notation):
        self.moves = re.split(moveRegex, notation)
        

    def getGameStates(self):
        return self.gameStates
