import pygame as p
from ChessEngine import GameState
from ChessEngine import Move
import SnailEngine
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15 # animations
IMAGES = {}

def LoadImages():
    """
    Initializes a global dictionary of images.
    """
    pieces = ['bP', 'bN', 'bB', 'bR', 'bQ', 'bK', 'wP', 'wN', 'wB', 'wR', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen  = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 14, False, False)
    gs = GameState()
    ValidMoves = gs.GetValidMoves()
    MoveMade = False # blank variable that flags when a move is made
    animate = False # flag variable for when we should animate a move
    LoadImages()
    running = True
    sqSelected = () # stores last click of the player
    playerClicks = [] # keeps track of player clicks 
    gameOver = False

    # human player or AI
    playerOne = True # if human is playing white, then this will be True, else False
    playerTwo = False # same as above but for black

    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # location of the mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected ==(row, col) or col >= 8: # player clicked the same square 2x or clicked outside the board
                        sqSelected = () # deselect
                        playerClicks = [] # clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                    if len(playerClicks) == 2 and humanTurn: #after 2nd click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(ValidMoves)):
                            if move == ValidMoves[i]:
                                gs.MakeMove(ValidMoves[i])
                                MoveMade = True
                                animate = True
                                sqSelected = () # reset player clicks
                                playerClicks = []
                        if not MoveMade:
                            playerClicks = [sqSelected]

            # key shortcuts
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo a move if 'z' is pressed
                    gs.UndoMove()
                    MoveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                    
                if e.key == p.K_r: # reset the game if 'r' is pressed
                    gs = GameState() # re-initialize the game state to reset the game
                    ValidMoves = gs.GetValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    MoveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

                if e.key ==p.K_e:
                    running = False # press 'e' to quit game
                    p.quit()    

        # AI move finder logic
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                returnQueue = Queue() # used to pass data between threads
                moveFinderProcess = Process(target=SnailEngine.findBestMove, args=(gs, ValidMoves, returnQueue))
                moveFinderProcess.start() # call findBestMove(gs, ValidMoves)

            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = SnailEngine.findRandomMove(ValidMoves)
                gs.MakeMove(AIMove)
                MoveMade = True
                animate = True
                AIThinking = False

        if MoveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            ValidMoves = gs.GetValidMoves()
            MoveMade = False
            animate = False
            moveUndone = False

        DrawGameState(screen, gs, ValidMoves, sqSelected, moveLogFont)

        if gs.CheckMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, 'Black wins by checkmate')
            else:
                drawEndGameText(screen, 'White wins by checkmate')
        elif gs.StaleMate:
            gameOver = True
            drawEndGameText(screen, 'Stalemate')
        
        clock.tick(MAX_FPS)
        p.display.flip()

def DrawGameState(screen, gs, ValidMoves, sqSelected, moveLogFont):
    """
    Draws all graphics
    """
    DrawBoard(screen) # draws squares
    highlightSquares(screen, gs, ValidMoves, sqSelected)
    DrawPieces(screen, gs.board)
    DrawMoveLog(screen, gs, moveLogFont)

def DrawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, ValidMoves, sqSelected):
    '''
    Responsible for all graphics within the current game state
    '''
    # TODO: highlight last move
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value -> 0 transparent, 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('green'))
            for move in ValidMoves:
                if move.StartRow == r and move.StartCol == c:
                    screen.blit(s, (move.EndCol*SQ_SIZE, move.EndRow*SQ_SIZE))

def DrawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def DrawMoveLog(screen, gs, font):
    '''
    Draw the move log
    '''
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveTexts), movesPerRow):
        text =""
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]

        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    '''
    Move Animations
    '''
    global colors
    coords = [] # list of coordinates that the animation will move through
    dR = move.EndRow - move.StartRow
    dC = move.EndCol - move.StartCol
    framesPerSquare = 8 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.StartRow + dR*frame/frameCount, move.StartCol + dC*frame/frameCount)
        DrawBoard(screen)
        DrawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.EndRow + move.EndCol)%2]
        endSquare = p.Rect(move.EndCol*SQ_SIZE, move.EndRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle
        if move.PieceCaptured != '--':
            if move.isEnPassantMove:
                enPassantRow = move.EndRow + 1 if move.PieceCaptured[0] == 'b' else move.EndRow - 1
                endSquare = p.Rect(move.EndCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.PieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.PieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 34, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Gray'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()


