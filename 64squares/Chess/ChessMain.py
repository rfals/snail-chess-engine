import pygame as p
from ChessEngine import GameState

WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # animations
IMAGES = ()

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
    print(gs.board)
    LoadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
            p.draw.rect(screen, color, p.rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def DrawPieces(screen, board):
    pass

if __name__ == "__main__":
    main()


