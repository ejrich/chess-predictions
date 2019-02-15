from Square import Square
from Color import Color
from Piece import Piece

def first(iterable, condition = lambda x : True):
    return next(x for x in iterable if condition(x))

class Board:
    def __init__(self):
        self.squares = []
        self.whitePieces = { Piece.Pawn: [], Piece.Rook: [], Piece.Bishop: [], Piece.Knight: [], Piece.Queen: [], Piece.King: [] }
        self.blackPieces = { Piece.Pawn: [], Piece.Rook: [], Piece.Bishop: [], Piece.Knight: [], Piece.Queen: [], Piece.King: [] }

        self.__initializeBoard()
        self.__initializePieces()

    def move(self, color, piece, currentFile, currentRank, newFile, newRank, promotion=None):
        # Set the current square to empty
        self.__setSquare(currentFile, currentRank, Color.Empty, '')

        # Get the current piece
        currentPiece = self.getPieceAtLocation(color, piece, currentFile, currentRank)

        currentPiece['file'] = newFile
        currentPiece['rank'] = newRank

        # Set the new square to the piece
        newSquare = self.squares[newFile][newRank]

        # Handle taken pieces
        if newSquare.piece:
            takenPiece = self.getPieceAtLocation(newSquare.color, newSquare.piece, newFile, newRank)
            if newSquare.color == Color.White:
                self.whitePieces[newSquare.piece].remove(takenPiece)
            elif newSquare.color == Color.Black:
                self.blackPieces[newSquare.piece].remove(takenPiece)
        # Handle En Passant - none in this dataset to I'm not handling them
        # elif captureFile != None and captureRank != None:
        #     capturedSquare = self.squares[captureFile][captureRank]
        #     if capturedSquare.color == Color.White:
        #         self.whitePieces[capturedSquare.piece] -= 1
        #     elif capturedSquare.color == Color.Black:
        #         self.blackPieces[capturedSquare.piece] -= 1

        self.__setSquare(newFile, newRank, color, piece)

        # Promote the piece if possible
        if promotion:
            if color == Color.White:
                self.whitePieces[piece].remove(currentPiece)
                self.whitePieces[promotion].append(currentPiece)
            elif color == Color.Black:
                self.blackPieces[piece].remove(currentPiece)
                self.blackPieces[promotion].append(currentPiece)

            self.__setSquare(newFile, newRank, color, promotion)

        self.color = color
        self.piece = piece
        self.currentFile = currentFile
        self.currentRank = currentRank
        self.newFile = newFile 
        self.newRank = newRank

    def getPieceAtLocation(self, color, piece, file=None, rank=None):
        pieces = self.whitePieces[piece] if color == Color.White else self.blackPieces[piece]

        if file == None and rank == None:
            return first(pieces)
        elif file != None and rank == None:
            return first(pieces, lambda x : x['file'] == file)
        elif file == None and rank != None:
            return first(pieces, lambda x : x['rank'] == rank)
        else:
            return first(pieces, lambda x : x['file'] == file and x['rank'] == rank)

    def getAllPieces(self, color, piece, file=None, rank=None):
        pieces = self.whitePieces[piece] if color == Color.White else self.blackPieces[piece]

        if file == None and rank == None:
            return pieces
        elif file != None and rank == None:
            return list(filter(lambda x : x['file'] == file, pieces))
        else:
            return list(filter(lambda x : x['rank'] == rank, pieces))

    def __initializeBoard(self):
        for file in range(8):
            self.squares.append([])
            for _ in range(8):
                self.squares[file].append(Square())

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
            if color == Color.White:
                self.whitePieces[Piece.Pawn].append({ 'file': file, 'rank': rank })
            else:
                self.blackPieces[Piece.Pawn].append({ 'file': file, 'rank': rank })

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

            if color == Color.White:
                self.whitePieces[piece].append({ 'file': file, 'rank': rank })
            else:
                self.blackPieces[piece].append({ 'file': file, 'rank': rank })
