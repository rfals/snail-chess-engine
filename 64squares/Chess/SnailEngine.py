import random


pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def findRandomMove(validMoves):
    '''
    Picks a random valid move
    '''
    return validMoves[random.randint(0, len(validMoves)-1)]


def findGreedyMove(gs, validMoves):
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
        # if the opponent is in checkmate or stalemate, the game is over, no need to go further
        if gs.StaleMate:
            opponentsMaxScore = STALEMATE
        elif gs.CheckMate:
            opponentsMaxScore = -CHECKMATE
        else:
            opponentsMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.MakeMove(opponentsMove)
                gs.GetValidMoves() # introduces inefficiency, but is necessary to check for checkmate and stalemate TODO: look for other solutions
                if gs.CheckMate:
                    score = CHECKMATE
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

def findBestMove(gs, validMoves):
    '''
    Helper method to find the first recursive call
    '''
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    '''
    Recursive function to find the best move using minimax algorithm
    '''
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves = gs.GetValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.UndoMove()
        return maxScore
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves = gs.GetValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.UndoMove()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    '''
    Recursive function to find the best move using negamax algorithm
    '''
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves = gs.GetValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.UndoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    '''
    Recursive function to find the best move using negamax algorithm
    '''
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    

    # move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves = gs.GetValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.UndoMove()
        if maxScore > alpha: #prune
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
           


def scoreBoard(gs):
    '''
    Score the board based on material, positive score is good for white, negative score is good for black
    '''
    if gs.CheckMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.StaleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score











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


