import numpy as np
import sys
import pygame
from pygame.locals import KEYDOWN, K_q

MAP = np.zeros((6,6), dtype=int)
cellMap = np.random.randint(3, size=(10,10))
SCREENSIZE = WIDTH, HEIGHT = 800, 600
#PADDING = PADDINGBOTTOM, PADDINGRIGHT = 60, 60
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
# GLOBAL VARS, Using a Dictionary.
_VARS = {'surf': False, 'gridWH': 400, 'gridCells': cellMap.shape[0],
         'gridOrigin': (200,100), 'lineWidth': 2}

# Press the green button in the gutter to run the script.

def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        #draw a grid
        drawSquareGrid(_VARS['gridOrigin'],_VARS['gridWH'],_VARS['gridCells'])
        #place cells
        placeCells()
        pygame.display.update()

def placeCells():
    cellBorder = 10
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    for row in range(cellMap.shape[0]):
        for column in range(cellMap.shape[1]):

            if(cellMap[column][row]==1):
                col = WHITE
            elif(cellMap[column][row]==2):
                col = BLACK
            else:
                col = GREY
            drawSquareCell(
                _VARS['gridOrigin'][0] + (celldimY*row)
                + cellBorder + (2*row*cellBorder) + _VARS['lineWidth']/2,
                _VARS['gridOrigin'][1] + (celldimY * column)
                + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                celldimX, celldimY, col)


def drawSquareCell(x, y, dimX, dimY, color):
    pygame.draw.rect(_VARS['surf'], color, (x, y, dimX, dimY))


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

def drawSquareGrid(origin, gridWH, cells):
    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y), (cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (CONTAINER_WIDTH_HEIGHT+cont_x, cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])

    cell_size = CONTAINER_WIDTH_HEIGHT/cells

    for x in range(cells):
        pygame.draw.line(_VARS['surf'],BLACK, (cont_x+(cell_size*x),0+cont_y),
                         (cont_x+(cell_size*x),CONTAINER_WIDTH_HEIGHT+cont_y),2)

    for y in range(cells):
        pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y+(cell_size*y)),
                         (cont_x+CONTAINER_WIDTH_HEIGHT, 0 + cont_y + (cell_size*y)), 2)


def drawLine():
    # draw a diagonal line from top left coordinates 0,0
    # to bottom right with coordinates 600 (Width), 400 (Height)
    pygame.draw.line(_VARS['surf'], BLACK, (0, 0), (WIDTH, HEIGHT), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (WIDTH, 0), (0, HEIGHT), 2)

if __name__ == '__main__':
    main()

