import re
from Board import Board
from Color import Color
from Piece import Piece

moveRegex = r'\s?\d+\.\s'

pawnMoveRegex = r'^([a-h])(\d)[+#]?$'
pawnCaptureRegex = r'^([a-h])x([a-h])(\d)[+#]?$'
namedMoveRegex = r'([KQRBN])([a-h])?(\d)?x?([a-h])(\d)[+#]?'
kingSideCastleRegex = r'^O-O[+#]?$'
queenSideCastleRegex = r'^O-O-O[+#]?$'
promotionRegex = r'^([a-h])(\d)=([QRBN])[+#]?$'
capturePromotionRegex = r'([a-h])x([a-h])(\d)=([QRBN])[+#]?'

decrement = lambda x : x - 1
same = lambda x : x
increment = lambda x : x + 1

class Game:
    def __init__(self):
        self.board = Board()
        self.properties = {}
        self.gameStates = []
        self.moves = []

    def setProperty(self, property, value):
        self.properties[property] = value

    def simulateGame(self, notation):
        self.moves = re.split(moveRegex, notation)

        for move in range(1, len(self.moves)):
            parts = self.moves[move].split(' ')
            # Last move of the game where only white moves
            if move == len(self.moves) - 1 and parts[1].startswith('{'):
                self.__makeMove(Color.White, parts[0])
                self.__addGameState()
            # Normal moves
            else:
                self.__makeMove(Color.White, parts[0])
                self.__addGameState()
                self.__makeMove(Color.Black, parts[1])
                self.__addGameState()

    # Mave the specified move and add a new game state
    def __makeMove(self, color, move):
        pawnMove = re.match(pawnMoveRegex, move)
        if pawnMove:
            self.__movePawn(color, pawnMove.group(1), pawnMove.group(2))
            return
        pawnCapture = re.match(pawnCaptureRegex, move)
        if pawnCapture:
            self.__pawnCapture(color, pawnCapture.group(1), pawnCapture.group(2), pawnCapture.group(3))
            return
        namedMove = re.match(namedMoveRegex, move)
        if namedMove:
            self.__moveNamed(color, Piece(namedMove.group(1)), namedMove.group(4), namedMove.group(5), namedMove.group(2), namedMove.group(3))
            return
        kingSideCastle = re.match(kingSideCastleRegex, move)
        if kingSideCastle:
            rank = 0 if color == Color.White else 7
            self.board.move(color, Piece.King, 4, rank, 6, rank)
            self.board.move(color, Piece.Rook, 7, rank, 5, rank)
            return
        queenSideCastle = re.match(queenSideCastleRegex, move)
        if queenSideCastle:
            rank = 0 if color == Color.White else 7
            self.board.move(color, Piece.King, 4, rank, 2, rank)
            self.board.move(color, Piece.Rook, 0, rank, 3, rank)
            return
        promotion = re.match(promotionRegex, move)
        if promotion:
            self.__movePawn(color, promotion.group(1), promotion.group(2), Piece(promotion.group(3)))
            return
        capturePromotion = re.match(capturePromotionRegex, move)
        if capturePromotion:
            self.__pawnCapture(color, capturePromotion.group(1), capturePromotion.group(2), capturePromotion.group(3), Piece(capturePromotion.group(4)))
            return
        print('Invalid move: ' + move)
        input()

    def __movePawn(self, color, file, rank, promotion=None):
        file = self.__translateFile(file)

        pawns = self.board.getAllPieces(color, Piece.Pawn, file - 1)

        if len(pawns) > 1:
            rankCompare = lambda x : x['rank'] < int(rank) - 1 if color == Color.White else lambda x : x['rank'] > int(rank) - 1
            pawns = list(filter(rankCompare, pawns))
            pawns = sorted(pawns, key=lambda x : x['rank'], reverse=color == Color.White)

        currentFile = pawns[0]['file']
        currentRank = pawns[0]['rank']
        self.board.move(color, Piece.Pawn, currentFile, currentRank, file - 1, int(rank) - 1, promotion)

    def __pawnCapture(self, color, previousFile, file, rank, promotion=None):
        previousFile = self.__translateFile(previousFile)
        file = self.__translateFile(file)

        pawns = self.board.getAllPieces(color, Piece.Pawn, previousFile - 1)

        if len(pawns) > 1:
            rankDifference = 2 if color == Color.White else 0
            piece = next(x for x in pawns if int(rank) - x['rank'] == rankDifference)
            # first(pawns, lambda x : x['rank'] - int(rank) == rankDifference)
            currentFile = piece['file']
            currentRank = piece['rank']
            self.board.move(color, Piece.Pawn, currentFile, currentRank, file - 1, int(rank) - 1, promotion)
        else:
            currentFile = pawns[0]['file']
            currentRank = pawns[0]['rank']
            self.board.move(color, Piece.Pawn, currentFile, currentRank, file - 1, int(rank) - 1, promotion)
    
    def __moveNamed(self, color, piece, file, rank, previousFile=None, previousRank=None):
        file = self.__translateFile(file)
        previousFile = self.__translateFile(previousFile) - 1 if previousFile else None
        previousRank = int(previousRank) - 1 if previousRank else None

        pieces = self.board.getAllPieces(color, piece, previousFile, previousRank)

        if len(pieces) > 1:
            if piece == Piece.Rook:
                movedPiece = self.__rookCanMove(pieces, file - 1, int(rank) - 1)
            elif piece == Piece.Bishop:
                movedPiece = self.__bishopCanMove(pieces, file - 1, int(rank) - 1)
            elif piece == Piece.Knight:
                movedPiece = self.__knightCanMove(pieces, file - 1, int(rank) - 1)

            currentFile = movedPiece['file']
            currentRank = movedPiece['rank']
            self.board.move(color, piece, currentFile, currentRank, file - 1, int(rank) - 1)
        else:
            currentFile = pieces[0]['file']
            currentRank = pieces[0]['rank']
            self.board.move(color, piece, currentFile, currentRank, file - 1, int(rank) - 1)

    def __translateFile(self, file):
        return ord(file) - 96 # 96 is one less that 'a'

    def __translateToFile(self, file):
        return chr(file + 97) # 97 is 'a'

    def __rookCanMove(self, pieces, file, rank):
        for piece in pieces:
            fileChange = abs(file - piece['file'])
            rankChange = abs(rank - piece['rank'])

            if fileChange > 0 and rankChange > 0:
                continue

            fileMove = same if fileChange == 0 else increment if file > piece['file'] else decrement
            rankMove = same if rankChange == 0 else increment if rank > piece['rank'] else decrement

            if self.__moveIterator(piece['file'], piece['rank'], file, rank, fileMove, rankMove):
                return piece

    def __bishopCanMove(self, pieces, file, rank):
        for piece in pieces:
            fileChange = abs(file - piece['file'])
            rankChange = abs(rank - piece['rank'])

            if fileChange != rankChange:
                continue

            fileMove = increment if file > piece['file'] else decrement
            rankMove = increment if rank > piece['rank'] else decrement

            if self.__moveIterator(piece['file'], piece['rank'], file, rank, fileMove, rankMove):
                return piece

    def __knightCanMove(self, pieces, file, rank):
        for piece in pieces:
            fileChange = abs(file - piece['file'])
            rankChange = abs(rank - piece['rank'])
            if fileChange == 2 and rankChange == 1 or fileChange == 1 and rankChange == 2:
                return piece

    def __moveIterator(self, currentFile, currentRank, file, rank, fileMove, rankMove):
        legal = True

        nextFile = fileMove(currentFile)
        nextRank = rankMove(currentRank)
        nextSquare = self.board.squares[nextFile][nextRank]

        while (not (nextFile == file and nextRank == rank) and legal):
            if nextSquare.piece:
                legal = False
            else:
                nextFile = fileMove(nextFile)
                nextRank = rankMove(nextRank)
                nextSquare = self.board.squares[nextFile][nextRank]

        return legal

    def __addGameState(self):
        # print()
        # for rank in reversed(range(8)):
        #     line = ''
        #     for file in range(8):
        #         piece = self.board.squares[file][rank].piece
        #         if piece:
        #             line += str(piece.value) + ' '
        #         else:
        #             line += '  '
        #     print(line)
        result = 1 if self.properties['Result'] == '1-0' else 0 if self.properties['Result'] == '0-1' else 0.5
        gameState = { 'Result': result }

        gameState['WhitePawns'] = len(self.board.whitePieces[Piece.Pawn])
        gameState['WhiteRooks'] = len(self.board.whitePieces[Piece.Rook])
        gameState['WhiteBishops'] = len(self.board.whitePieces[Piece.Bishop])
        gameState['WhiteKnights'] = len(self.board.whitePieces[Piece.Knight])
        gameState['WhiteQueen'] = len(self.board.whitePieces[Piece.Queen])
        gameState['WhiteKing'] = len(self.board.whitePieces[Piece.King])
        gameState['WhiteTotal'] = gameState['WhitePawns'] + gameState['WhiteRooks'] + gameState['WhiteBishops'] + gameState['WhiteKnights'] + gameState['WhiteQueen'] + gameState['WhiteKing']

        gameState['BlackPawns'] = len(self.board.blackPieces[Piece.Pawn])
        gameState['BlackRooks'] = len(self.board.blackPieces[Piece.Rook])
        gameState['BlackBishops'] = len(self.board.blackPieces[Piece.Bishop])
        gameState['BlackKnights'] = len(self.board.blackPieces[Piece.Knight])
        gameState['BlackQueen'] = len(self.board.blackPieces[Piece.Queen])
        gameState['BlackKing'] = len(self.board.blackPieces[Piece.King])
        gameState['BlackTotal'] = gameState['BlackPawns'] + gameState['BlackRooks'] + gameState['BlackBishops'] + gameState['BlackKnights'] + gameState['BlackQueen'] + gameState['BlackKing']

        for rank in range(8):
            for file in range(8):
                square = self.board.squares[file][rank]
                actualFile = self.__translateToFile(file)
                gameState[actualFile + str(rank + 1) + '_color'] = square.color.value
                gameState[actualFile + str(rank + 1) + '_piece'] = square.piece.value if square.piece != '' else ''

        self.gameStates.append(gameState)
