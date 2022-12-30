import pygame as p
from ChessEngine import GameState
from ChessEngine import Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
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
    screen  = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    ValidMoves = gs.GetValidMoves()
    MoveMade = False # blank variable that flags when a move is made

    print(gs.board)
    LoadImages()
    running = True
    sqSelected = () # stores last click of the player
    playerClicks = [] # keeps track of player clicks 
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected ==(row, col): # player clicked the same square
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
                if len(playerClicks) ==2: #after 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.GetChessNotation())
                    for i in range(len(ValidMoves)):
                        if move == ValidMoves[i]:
                            gs.MakeMove(move)
                            MoveMade = True

                            sqSelected = () # reset player clicks
                            playerClicks = []
                    if not MoveMade:
                        playerClicks = [sqSelected]

                # key shortcuts
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo a move if 'z' is pressed
                    gs.UndoMove()
                    MoveMade = True

                if e.key ==p.K_e:
                    running = False # press 'e' to quit game
                    p.quit()    

        if MoveMade:
            ValidMoves = gs.GetValidMoves()
            MoveMade = False

        DrawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def DrawGameState(screen, gs):
    """
    Draws all graphics
    """
    DrawBoard(screen) # draws squares
    #TODO: draw legal moves
    DrawPieces(screen, gs.board)

def DrawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def DrawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()


