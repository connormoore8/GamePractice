import numpy as np
import sys
import pygame
from pygame.locals import KEYDOWN, K_q, K_SPACE


def main():
    pygame.init()
    font = pygame.font.Font(None, 32)
    delay = 10
    # Initial Setup
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    #print(_VARS['cellMap'])
    _VARS['input'] = pygame.draw.rect(_VARS['surf'], 'black', (0+0, 0, 800, 100))
    while True:
        checkEvents()
        pygame.time.wait(delay)
        txt_surface = font.render(_VARS['text'], True, 'white')
        _VARS['surf'].fill(GREY)
        _VARS['input'] = pygame.draw.rect(_VARS['surf'], 'black', (0, 0, 800, 100))
        # draw a grid
        if _VARS['gridSetup']:
            #print(_VARS['gridCells'])
            _VARS['cellMap'] = np.zeros((_VARS['gridCells'] + 6, _VARS['gridCells'] + 6), dtype=int)
            nextGen = np.zeros((_VARS['gridCells'] + 6, _VARS['gridCells'] + 6), dtype=int)
            _VARS['gridSetup'] = False
        if len(_VARS['cellMap']) > 0:
            drawSquareGrid(_VARS['gridOrigin'], _VARS['gridWH'], _VARS['gridCells'])
            #print('drawn')
            # place cells
        # update entry
        if _VARS['start'] and _VARS['state']:
            delay = 250
            for x in range(_VARS['cellMap'].shape[1]):
                for y in range(_VARS['cellMap'].shape[0]):
                    examineCell(x, y, nextGen)
            _VARS['cellMap'] = nextGen
            #print(_VARS['cellMap'])

        #print(len(_VARS['text']))
        placeCells()
        _VARS['surf'].blit(txt_surface, (WIDTH/2 - 5*len(_VARS['text']), _VARS['input'].y + 45))
        pygame.display.update()
        nextGen = np.zeros((_VARS['gridCells'] + 6, _VARS['gridCells'] + 6), dtype=int)


def examineCell(i, j, nextGen):
    # sum N Neighbors:
    edge = _VARS['gridCells'] + 5
    if i == 0 or i == edge or j == 0 or j == edge:
        nextGen[j][i] = 0
        return
    total = 0
    for x in range(3):
        for y in range(3):
            total += _VARS['cellMap'][j+y-1][i+x-1]
    if _VARS['cellMap'][j][i] == 1:
        if total == 3 or total == 4:
            # update new cellMap
            nextGen[j][i] = 1
        else:
            nextGen[j][i] = 0
    else:
        if total == 3:
            # print('reproduce')
            nextGen[j][i] = 1
        else:
            nextGen[j][i] = 0
    # print(nextGen)


def placeCells():
    if _VARS['gridCells'] > 0:
        cellBorder = (_VARS['gridWH']/_VARS['gridCells'])*.15
        celldimX = celldimY = (_VARS['gridWH'] / _VARS['gridCells']) - (cellBorder * 2)
        for row in range(_VARS['cellMap'].shape[0] - 6):
            for column in range(_VARS['cellMap'].shape[1] - 6):
                if _VARS['cellMap'][column + 3][row + 3] == 1:
                    col = WHITE
                # elif(cellMap[column][row]==2):
                #    col = BLACK
                else:
                    col = GREY
                drawSquareCell(
                    _VARS['gridOrigin'][0] + (celldimY * row)
                    + cellBorder + (2 * row * cellBorder) + _VARS['lineWidth'] / 2,
                    _VARS['gridOrigin'][1] + (celldimY * column)
                    + cellBorder + (2 * column * cellBorder) + _VARS['lineWidth'] / 2,
                    celldimX, celldimY, col)




def drawSquareCell(x, y, dimX, dimY, color):
    pygame.draw.rect(_VARS['surf'], color, (x, y, dimX, dimY))


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if _VARS['input'].collidepoint(event.pos):
                _VARS['KeyBoardInput'] = True
                _VARS['text'] = ""
            else:
                _VARS['KeyBoardInput'] = False
        if event.type == pygame.MOUSEBUTTONUP and len(_VARS['cellMap']) > 0:
            pos = pygame.mouse.get_pos()
            # print(pos)
            # convert to position on board.
            coord = indexPicker(pos, 1), indexPicker(pos, 0)
            #print(coord)
            # update cellBoard
            #original without buffer
            #_VARS['cellMap'][coord[0]][coord[1]] = 1
            _VARS['cellMap'][coord[0]+3][coord[1]+3] = 1
            #print(_VARS['cellMap'])
        if event.type == KEYDOWN:
            if _VARS['KeyBoardInput']:
                if event.key == pygame.K_RETURN:
                    #print(_VARS['text'])
                    #try to convert text to numbers.
                    _VARS['gridCells'] = text_interpretor(_VARS['text'])
                    _VARS['text'] = "Click on Squares to Activate Cell, and press 'Space' to start the game!"
                    _VARS['start'] = True
                    _VARS['gridSetup'] = True
                elif event.key == pygame.K_BACKSPACE:
                    _VARS['text'] =_VARS['text'][:-1]
                else:
                    _VARS['text'] += event.unicode
        if event.type == KEYDOWN and event.key == K_SPACE:
            _VARS['state'] = True
        if event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

def text_interpretor(text):
    result = ''
    for char in text:
        if char.isnumeric():
            result += char
    return int(result)

def indexPicker(mousePos, axis):
    indexList = [_VARS['gridOrigin'][axis] + (_VARS['gridWH']/_VARS['gridCells'])*x for x in range(_VARS['gridCells'])]
    index = -1
    for element in indexList:
        if mousePos[axis] < element:
            return index
        index += 1
    return _VARS['gridCells']-1

def drawSquareGrid(origin, gridWH, cells):
    CONTAINER_WIDTH_HEIGHT = gridWH
    cont_x, cont_y = origin
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y), (cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])
    pygame.draw.line(_VARS['surf'], BLACK, (CONTAINER_WIDTH_HEIGHT+cont_x, cont_y), (CONTAINER_WIDTH_HEIGHT+cont_x, CONTAINER_WIDTH_HEIGHT+cont_y), _VARS['lineWidth'])

    cell_size = CONTAINER_WIDTH_HEIGHT/cells

    for x in range(cells):
        pygame.draw.line(_VARS['surf'], BLACK, (cont_x+(cell_size*x), 0+cont_y),
                         (cont_x+(cell_size*x), CONTAINER_WIDTH_HEIGHT+cont_y), 2)

    for y in range(cells):
        pygame.draw.line(_VARS['surf'], BLACK, (cont_x, cont_y+(cell_size*y)),
                         (cont_x+CONTAINER_WIDTH_HEIGHT, 0 + cont_y + (cell_size*y)), 2)


def drawLine():
    # draw a diagonal line from top left coordinates 0,0
    # to bottom right with coordinates 600 (Width), 400 (Height)
    pygame.draw.line(_VARS['surf'], BLACK, (0, 0), (WIDTH, HEIGHT), 2)
    pygame.draw.line(_VARS['surf'], BLACK, (WIDTH, 0), (0, HEIGHT), 2)

if __name__ == '__main__':
    # cellMap = np.random.randint(2, size=(10, 10))
    MAP = np.zeros((6, 6), dtype=int)
    SCREENSIZE = WIDTH, HEIGHT = 800, 800
    # PADDING = PADDINGBOTTOM, PADDINGRIGHT = 60, 60
    BLACK = (0, 0, 0)
    GREY = (160, 160, 160)
    WHITE = (255, 255, 255)

    # cellMap = np.random.randint(2, size=(10,10))
    # random state: np.random.randint(2, size=(15,15))
    # board[2] = [0,0,0,1,1,1,0,0,0,1,1,1,0,0,0]
    # board[6] = [0 for x in range(6)] + [1,1] + [0 for x in range(7)]
    # board[7] = [0 for x in range(6)] + [1,1] + [0 for x in range(7)]
    # [1 for x in range(board.shape[0])]
    text = ''
    # GLOBAL VARS, Using a Dictionary
    _VARS = {'surf': False, 'gridWH': 500, 'gridCells': 0,
             'gridOrigin': (150, 150), 'lineWidth': 2,
             'cellMap': np.array([]), 'gridSetup': False,
             'state': False, 'input': False, 'start': False,
             'text': 'Base Dimension: 25, click on this box to adjust it', 'KeyBoardInput': False}

    main()

