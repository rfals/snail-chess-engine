"""
Class responsible for storing info and determining legal moves.
"""


class GameState():
    def __init__(self) -> None:
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], # Backrank black pieces
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"], # Black pawns
            ["--", "--", "--", "--", "--", "--", "--", "--"], # Empty squares
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []

    def MakeMove(self, move):
        self.board[move.StartRow][move.StartCol] = "--"
        self.board[move.EndRow][move.EndCol] = move.PieceMoved
        self.moveLog.append(move) # store the move
        self.whiteToMove = not self.whiteToMove # swap turns
class Move():

    # Dictionaries that map keys to values to have a proper chess notation

    RanksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
    "5": 3, "6": 2, "7": 1, "8": 0}

    RowsToRanks = {v: k for k, v in RanksToRows.items()}

    FilesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
    "e": 4, "f": 5, "g": 6, "h": 7}

    ColsToFiles = {v: k for k, v in FilesToCols.items()}


    def __init__(self, StartSq, EndSq, board) -> None:
        self.StartRow = StartSq[0]
        self.StartCol = StartSq[1]
        self.EndRow = EndSq[0]
        self.EndCol = EndSq[1]
        self.PieceMoved = board[self.StartRow][self.StartCol]
        self.PieceCaptured = board[self.EndRow][self.EndCol]

    def GetChessNotation(self):
        # TODO: reverse c and r to have the proper proper chess notation
        return self.GetRankFile(self.StartRow, self.StartCol) + self.GetRankFile(self.EndRow, self.EndCol)
    
    def GetRankFile(self, r, c):
        return self.ColsToFiles[c] + self.RowsToRanks[r]











    