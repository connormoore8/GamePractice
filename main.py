import numpy as np
import sys
import pygame
from pygame.locals import KEYDOWN, K_q

MAP = np.zeros((6,6), dtype=int)

SCREENSIZE = WIDTH, HEIGHT = 800, 600
#PADDING = PADDINGBOTTOM, PADDINGRIGHT = 60, 60
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
#cellMap = np.random.randint(2, size=(10,10))
# GLOBAL VARS, Using a Dictionary.
# random state: np.random.randint(2, size=(15,15))
board = np.zeros((15,15),dtype=int)
#board[2] = [0,0,0,1,1,1,0,0,0,1,1,1,0,0,0]
#board[6] = [0 for x in range(6)] + [1,1] + [0 for x in range(7)]
#board[7] = [0 for x in range(6)] + [1,1] + [0 for x in range(7)]
    #[1 for x in range(board.shape[0])]
_VARS = {'surf': False, 'gridWH': 500, 'gridCells': 15,
         'gridOrigin': (150,50), 'lineWidth': 2,
         'cellMap':board}

# Press the green button in the gutter to run the script.

def main():
    pygame.init()  # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    print(_VARS['cellMap'])
    while True:
        checkEvents()

        pygame.time.wait(500)
        _VARS['surf'].fill(GREY)
        nextGen = np.zeros((_VARS['gridCells'], _VARS['gridCells']),dtype=int)
        #draw a grid
        drawSquareGrid(_VARS['gridOrigin'],_VARS['gridWH'],_VARS['gridCells'])
        #place cells
        placeCells()
        #update entry
        #for x in range(_VARS['cellMap'].shape[1]):
        #    for y in range(_VARS['cellMap'].shape[0]):
        #        examineCell(x, y, nextGen)
        #_VARS['cellMap'] = nextGen
        pygame.display.update()


def examineCell(i, j, nextGen):
    #sum N Neighbors:
    edge = _VARS['gridCells'] - 1
    if i==0 or i == edge or j ==0 or j == edge:
        nextGen[j][i]=0
        return
    total = 0
    for x in range(3):
        for y in range(3):
            total += _VARS['cellMap'][j+y-1][i+x-1]
    if _VARS['cellMap'][j][i]==1:
        if total == 3 or total == 4:
            #print('survive')
            nextGen[j][i] = 1
            #update new cellMap
        else:
            nextGen[j][i] = 0
    else:
        if total == 3:
            #print('reproduce')
            nextGen[j][i] = 1
        else:
            nextGen[j][i] = 0
    #print(nextGen)

def placeCells():
    cellBorder = 10
    celldimX = celldimY = (_VARS['gridWH']/_VARS['gridCells']) - (cellBorder*2)
    for row in range(_VARS['cellMap'].shape[0]):
        for column in range(_VARS['cellMap'].shape[1]):

            if(_VARS['cellMap'][column][row]==1):
                col = WHITE
            #elif(cellMap[column][row]==2):
            #    col = BLACK
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
        #handle mouse events
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #print(pos)
            print(indexPicker(pos,0), indexPicker(pos,1))
            #convert to position on board.

        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

def indexPicker(mousePos, axis):
    indexList = [_VARS['gridOrigin'][axis]  + (_VARS['gridWH']/_VARS['gridCells'])*x for x in range(_VARS['gridCells'])]
    index = -1
    for element in indexList:
        if mousePos[axis] < element:
            return index
        index +=1
    return 14






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
    #cellMap = np.random.randint(2, size=(10, 10))
    main()

