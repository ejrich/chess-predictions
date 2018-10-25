import re
from Board import Board
from Color import Color

moveRegex = r'\s?\d+\.\s'

pawnMoveRegex = r'^([a-h])(\d)[+#]?$'
pawnCaptureRegex = r'^([a-h])x([a-h])(\d)[+#]?$'
namedMoveRegex = r'([KQRBN])([a-h]?\d?)x?([a-h])(\d)[+#]?'
kingSideCastleRegex = r'O-O[+#]?'
queenSideCastleRegex = r'O-O-O[+#]?'
promotionRegex = r'([a-h])(\d)=([QRBN])[+#]?'

class Game:
    properties = {}
    gameStates = []
    moves = []

    def __init__(self):
        self.board = Board()

    def setProperty(self, property, value):
        self.properties[property] = value

    def simulateGame(self, notation):
        self.moves = re.split(moveRegex, notation)

        for move in range(1, len(self.moves)):
            parts = self.moves[move].split(' ')
            # Last move of the game where only white moves
            if move == len(self.moves) - 1 and parts[1].startswith('{'):
                self.__makeMove(Color.White, parts[0])
            # Normal moves
            else:
                self.__makeMove(Color.White, parts[0])
                self.__makeMove(Color.Black, parts[1])

    # Mave the specified move and add a new game state
    def __makeMove(self, color, move):
        pawnMove = re.match(pawnMoveRegex, move)
        if pawnMove:
            # Do something
            return
        pawnCapture = re.match(pawnCaptureRegex, move)
        if pawnCapture:
            # Do something
            return
        namedMove = re.match(namedMoveRegex, move)
        if namedMove:
            # Do something
            return
        kingSideCastle = re.match(kingSideCastleRegex, move)
        if kingSideCastle:
            # Do something
            return
        queenSideCastle = re.match(queenSideCastleRegex, move)
        if queenSideCastle:
            # Do something
            return
        promotion = re.match(promotionRegex, move)
        if promotion:
            # Do something
            return
        print('Invalid move: ' + move)
        input()


    def getGameStates(self):
        return self.gameStates
