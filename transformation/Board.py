from Square import Square
from Color import Color
from Piece import Piece

class Board:
    squares = []
    whitePieces = { Piece.Pawn: 8, Piece.Rook: 2, Piece.Bishop: 2, Piece.Knight: 2, Piece.Queen: 1, Piece.King: 1 }
    blackPieces = { Piece.Pawn: 8, Piece.Rook: 2, Piece.Bishop: 2, Piece.Knight: 2, Piece.Queen: 1, Piece.King: 1 }

    def __init__(self):
        self.__initializeBoard()
        self.__initializePieces()

    def move(self, color, piece, currentFile, currentRank, newFile, newRank, captureFile=None, captureRank=None, promotion=None):
        # Set the current square to empty
        self.__setSquare(currentFile, currentRank, None, None)
        # Set the new square to the piece
        newSquare = self.squares[newFile][newRank]

        if newSquare.piece:
            if newSquare.color == Color.White:
                self.whitePieces[newSquare.piece] -= 1
            elif newSquare.color == Color.Black:
                self.blackPieces[newSquare.piece] -= 1
        elif captureFile != None and captureRank != None:
            capturedSquare = self.squares[captureFile][captureRank]
            if capturedSquare.color == Color.White:
                self.whitePieces[capturedSquare.piece] -= 1
            elif capturedSquare.color == Color.Black:
                self.blackPieces[capturedSquare.piece] -= 1

        self.__setSquare(newFile, newRank, color, piece)

        if promotion != None:
            self.__setSquare(newFile, newRank, color, promotion)

    def __initializeBoard(self):
        for file in range(8):
            self.squares[file] = [] 
            for rank in range(8):
                self.squares[file][rank] = Square()

    def __initializePieces(self):
        self.__initializeHomeRank(Color.White, 0)
        self.__initializePawns(Color.White, 1)

        self.__initializeHomeRank(Color.Black, 7)
        self.__initializePawns(Color.Black, 6)

    def __setSquare(self, file, rank, color, piece):
        self.squares[file][rank].color = color
        self.squares[file][rank].piece = piece

    def __initializePawns(self, color, rank):
        for file in range(8):
            self.__setSquare(file, rank, color, Piece.Pawn)

    def __initializeHomeRank(self, color, rank):
        for file in range(8):
            piece = None

            if file == 0 or file == 7:
                piece = Piece.Rook
            elif file == 1 or file == 6:
                piece = Piece.Knight
            elif file == 2 or file == 5:
                piece = Piece.Bishop
            elif file == 3:
                piece = Piece.Queen
            elif file == 4:
                piece = Piece.King

            self.__setSquare(file, rank, color, piece)
