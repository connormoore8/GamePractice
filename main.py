import sys
import pygame
from pygame.locals import KEYDOWN, K_q

SCREENSIZE = WIDTH, HEIGHT = 600, 400
#PADDING = PADDINGBOTTOM, PADDINGRIGHT = 60, 60
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
# GLOBAL VARS, Using a Dictionary.
_VARS = {'surf': False}

# Press the green button in the gutter to run the script.

def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        #drawLine()
        drawGrid(5)
        pygame.display.update()

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

def drawGrid(divisions):
    CONTAINER_WIDTH_HEIGHT = 300
    cont_x, cont_y =10, 10

    drawRect(cont_x, cont_y, CONTAINER_WIDTH_HEIGHT)
    cell_size = CONTAINER_WIDTH_HEIGHT/divisions

    for x in range(divisions):
        pygame.draw.line(_VARS['surf'],BLACK, (cont_x+(cell_size*x),0+cont_y),
                         (cont_x+(cell_size*x),CONTAINER_WIDTH_HEIGHT+cont_y),2)

    for y in range(divisions):
        pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y+(cell_size*y)),
                         (cont_x+CONTAINER_WIDTH_HEIGHT, 0 + cont_y + (cell_size*y)), 2)


def drawRect(x, y, Size):
    pygame.draw.line(_VARS['surf'], BLACK, (x,y), (Size + x, y), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (x,y), (x, Size + y), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (x, Size + y), (Size + x, Size + y), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (Size + x, y),(Size + x, Size + y), 2)


def drawLine():
    # draw a diagonal line from top left coordinates 0,0
    # to bottom right with coordinates 600 (Width), 400 (Height)
    pygame.draw.line(_VARS['surf'], BLACK, (0, 0), (WIDTH, HEIGHT), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (WIDTH, 0), (0, HEIGHT), 2)

if __name__ == '__main__':
    main()

