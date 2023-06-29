import random


pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(validMoves):
    '''
    Picks a random valid move
    '''
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):
    '''
    Finds the best move based on material only
    '''

    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.MakeMove(playerMove)
        opponentsMoves = gs.GetValidMoves()
        opponentsMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.MakeMove(opponentsMove)
            if gs.CheckMate:
                score = - turnMultiplier * CHECKMATE
            elif gs.StaleMate:
                score = STALEMATE
            else:
                score = - turnMultiplier * scoreMaterial(gs.board)
            if score > opponentsMaxScore:
                opponentsMaxScore = score
            gs.UndoMove()
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.UndoMove()
    return bestPlayerMove

def scoreMaterial(board):
    '''	
    Svore the board based on material.
    '''
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score


