

class GameState():
    """
    Class responsible for storing info and determining legal moves.
    """

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
        self.MoveFunctions = {'P': self.GetPawnMoves, 'N': self.GetNightMoves, 'B': self.GetBishopMoves,
        'R': self.GetRookMoves, 'Q':self.GetQueenMoves, 'K': self.GetKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.WhiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)
        self.CheckMate = False
        self.StaleMate = False

    def MakeMove(self, move):
        """
        Takes a move given as param and executes it.
        """
        self.board[move.StartRow][move.StartCol] = "--"
        self.board[move.EndRow][move.EndCol] = move.PieceMoved
        self.moveLog.append(move) # store the move
        self.whiteToMove = not self.whiteToMove # swap turns

        # Update Kings Location
        if move.PieceMoved == "wK":
            self.WhiteKingLocation = (move.EndRow, move.EndCol)
        elif move.PieceMoved == "bK":
            self.BlackKingLocation = (move.EndRow, move.EndCol)

        # Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.EndRow][move.EndCol] = move.PieceMoved[0] + 'Q'


    def UndoMove(self):
        if len(self.moveLog) != 0: # can only undo if a move is made
            move = self.moveLog.pop()
            self.board[move.StartRow][move.StartCol] = move.PieceMoved
            self.board[move.EndRow][move.EndCol] = move.PieceCaptured
            self.whiteToMove = not self.whiteToMove # switch back turns

            # Update Kings Location
            if move.PieceMoved == "wK":
                self.WhiteKingLocation = (move.StartRow, move.StartCol)
            elif move.PieceMoved == "bK":
                self.BlackKingLocation = (move.StartRow, move.StartCol)

    def GetValidMoves(self):
        """
        All moves besides checks
        """
        # 1) Generate all possible moves
        moves = self.GetPossibleMoves()

        # 2) for each move, make the move
        for i in range(len(moves) -1, -1, -1): # when removing from a list go backward so the indexes dont shift
            self.MakeMove(moves[i])

        # 3) generate all opponent's moves
        # 4) for each opponents moves see if they attack your king
            self.whiteToMove = not self.whiteToMove # switch turns so InCheck works
            if self.InCheck():
                moves.remove(moves[i])
        # 5) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.UndoMove()
        
        if len(moves) == 0: # either checkmate or stalemate
            if self.InCheck():
                self.CheckMate = True
            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False


        return moves

    def InCheck(self):
        """
        Determines if the player is in check
        """
        if self.whiteToMove:
            return self.SquareUnderAttack(self.WhiteKingLocation[0], self.WhiteKingLocation[1])
        else:
            return self.SquareUnderAttack(self.BlackKingLocation[0], self.BlackKingLocation[1])

    def SquareUnderAttack(self, r, c):
        """
        Determins if the enemy can attack the square at r,c
        """
        self.whiteToMove = not self.whiteToMove # switch to opponents POV
        OppMoves = self.GetPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch back turns
        for move in OppMoves:
            if move.EndRow == r and move.EndCol == c: # square is under attack
                return True
        return False




    def GetPossibleMoves(self):
        """
        GetAllValidMoves + Invalid moves
        """
        moves  = []
        for r in range(len(self.board)): # nr. of rows
            for c in range(len(self.board[r])): # nr. of columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn =='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # calls the appropriate move function based on piece type
                    self.MoveFunctions[piece](r,c,moves) # using dictionaries instead of 6 'if' statements
        return moves

    def GetPawnMoves(self,r,c,moves):
        """
        Get all the pawn moves for the pawn located at r,c and add the moves to list
        """
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            # captures to the left
            if c - 1 >= 0: # because we dont want column -1
                if self.board[r-1][c-1][0] == 'b': # enemy pice to capture
                   moves.append(Move((r, c), (r-1, c-1), self.board))
            # captures to the right
            if c + 1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c),(r-1, c+1), self.board))
        
        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            # captures to the left
            if c - 1 >= 0: # because we dont want column -1
                if self.board[r+1][c-1][0] == 'w': # enemy pice to capture
                   moves.append(Move((r, c), (r+1, c-1), self.board))
            # captures to the right
            if c + 1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c),(r+1, c+1), self.board))

    def GetNightMoves(self,r,c,moves):
        """
        Get all the knight moves for the knight located at r,c and add the moves to list
        """
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1),(2, 1))  # directions: up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            EndRow = r + m[0]
            EndCol = c + m[1]
            if 0 <= EndRow <= 7 and 0 <= EndCol <= 7: # check for possible moves
                EndPiece = self.board[EndRow][EndCol]
                if EndPiece[0] != ally_color:
                    moves.append(Move((r, c), (EndRow, EndCol), self.board))

    def GetBishopMoves(self,r,c,moves):
        """
        Get all the bishop moves for the bishop located at r,c and add the moves to list
        """
        directions = ((-1,-1), (-1,1), (1,1), (1,-1)) # directions: diagonals
        enemy_color = 'b' if self.whiteToMove else 'w'
        for direction in directions:
            for i in range(1, 8):
                EndRow = r + direction[0] * i
                EndCol = c + direction[1] * i
                if 0 <= EndRow <= 7 and 0 <= EndCol <= 7: # check for possible moves
                    EndPiece = self.board[EndRow][EndCol]
                    if EndPiece == "--": # if empty space, then we can move the bishop there
                        moves.append(Move((r, c), (EndRow, EndCol), self.board))
                    elif EndPiece[0] == enemy_color: # enemy piece valid
                        moves.append(Move((r, c), (EndRow, EndCol), self.board))
                        break
                    else: # same color piece invalid
                        break
                else: # off board
                    break

    def GetRookMoves(self,r,c,moves):
        """
        Get all the rook moves for the rook located at r,c and add the moves to list
        """
        directions = ((-1,0), (0,-1), (1,0), (0,1)) # directions: up,left,down,right
        enemy_color = 'b' if self.whiteToMove else 'w'
        for direction in directions:
            for i in range(1, 8):
                EndRow = r + direction[0] * i
                EndCol = c + direction[1] * i
                if 0 <= EndRow <= 7 and 0 <= EndCol <= 7: # check for possible moves
                    EndPiece = self.board[EndRow][EndCol]
                    if EndPiece == "--": # if empty space, then we can move the rook there
                        moves.append(Move((r, c), (EndRow, EndCol), self.board))
                    elif EndPiece[0] == enemy_color: # enemy piece valid
                        moves.append(Move((r, c), (EndRow, EndCol), self.board))
                        break
                    else: # same color piece invalid
                        break
                else: # off board
                    break

    def GetQueenMoves(self,r,c,moves):
        """
        Get all the queen moves for the queen located at r,c and add the moves to list
        """
        self.GetRookMoves(r,c,moves)
        self.GetBishopMoves(r,c,moves)

    def GetKingMoves(self, r, c, moves):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        directions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            EndRow = r + directions[i][0]
            EndCol = c + directions[i][1]
            if 0 <= EndRow <= 7 and 0 <= EndCol <= 7:
                EndPiece = self.board[EndRow][EndCol]
                if EndPiece[0] != ally_color: # not an ally piece or an empty piece
                    moves.append(Move((r,c), (EndRow, EndCol), self.board))


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
        self.isPawnPromotion = False
        if (self.PieceMoved == "wP" and self.EndRow == 0) or (self.PieceMoved == "bP" and self.EndRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.StartRow * 1000 + self.StartCol * 100 + self.EndRow* 10 + self.EndCol # same as having a hash function that outputs 4 digits
        #print(self.moveID)

    def __eq__(self, other):
        """
        Overriding the equals method
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def GetChessNotation(self):
        # TODO: reverse c and r to have the proper proper chess notation
        return self.GetRankFile(self.StartRow, self.StartCol) + self.GetRankFile(self.EndRow, self.EndCol)
    
    def GetRankFile(self, r, c):
        return self.ColsToFiles[c] + self.RowsToRanks[r]











    