# events-example0.py
# Barebones timer, mouse, and keyboard events


from tkinter import *
import random
import copy

# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################


####################################
# customize these functions
####################################
def initBoard(data):
    data.board1 = [[1,1,1,0,0,0,0,0,0,0],
                    [1,1,1,1,1,1,0,0,0,0],
                    [1,1,1,1,1,1,1,1,1,1],
                    [0,1,1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,1,1,-1,1,1],
                    [0,0,0,0,0,0,1,1,1,0]]
    data.board2 = [[0,0,0,0,0,0,1,1,1,1,0,0,1,1,1],
         [1,1,1,1,0,0,1,1,3,1,0,0,1,-1,1],
         [1,1,2,1,0,0,1,1,1,1,0,0,1,1,1],
         [1,1,1,1,0,0,1,1,1,1,0,0,1,1,1],
         [1,1,1,1,0,0,1,1,1,1,0,0,1,1,1],
         [1,1,1,1,0,0,1,1,1,1,0,0,0,0,0]]
    data.board3 = [[0,0,0,4,4,4,4,4,4,4,0,0,0,0],
         [0,0,0,4,4,4,4,4,4,4,0,0,0,0],
         [1,1,1,1,0,0,0,0,0,1,1,1,0,0],
         [1,1,1,0,0,0,0,0,0,0,1,1,0,0],
         [1,1,1,0,0,0,0,0,0,0,1,1,0,0],
         [1,1,1,0,0,1,1,1,1,4,4,4,4,4],
         [1,1,1,0,0,1,1,1,1,4,4,4,4,4],
         [0,0,0,0,0,1,-1,1,0,0,4,4,1,4],
         [0,0,0,0,0,1,1,1,0,0,4,4,4,4]]
    data.board4 = [[0,0,0,0,0,0,0,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,1,1,1,0,0,0],
         [1,1,1,1,1,1,0,1,1,1,1,1,1],
         [1,1,1,1,5,1,0,1,1,1,1,-1,1],
         [1,1,1,1,1,1,0,1,1,1,1,1,1],
         [0,0,0,0,0,0,0,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,1,1,1,0,0,0],
         [0,0,0,0,0,0,0,1,1,1,0,0,0]]
    # boardi is 2-d list of map. 
    data.level1 = {'board': data.board1, 'start': (1,1), 'target': (4,7)}
    data.level2 = {'board': data.board2, 'start': (4,1), 
                'softBridge':[[(4,4),(4,5)]], 'hardBridge': [[(4,10),(4,11)]], 
                'target': (1,13)}
    data.level3 = {'board': data.board3, 'start': (5,1), 'target':(7,6)}
    data.level4 = {'board':data.board4, 'start':(4,1),
                'dividedPosition':[[(1,8), (7,8)]], 'target': (4,11)}
    data.levels = [data.level1, data.level2, data.level3, data.level4]
    data.curLevel = data.level1
    data.curBoard = data.board1
    data.levelNum = 0

def initSolution(data):
    if (('softBridge' not in data.curLevel) 
        and ('hardBridge' not in data.curLevel)
        and ('dividedPosition' not in data.curLevel)):
        initSolveByItself(data)
    else:
        data.solution = None
        
def init(data):
    initBoard(data)
    instructionInit(data)
    designInit(data)
    data.blockNum = 1
    data.step = 0
    data.mode = 'startingSplash'
    data.image = PhotoImage(file="tile1.png")
    data.blockImage = PhotoImage(file='block1.png')
    data.blockImage2 = PhotoImage(file='block2.png')
    data.blockImage3 = PhotoImage(file='block3.png')
    data.dBlockImage = PhotoImage(file='dblock.png')
    data.blockFall1 = PhotoImage(file='fall1.png')
    data.blockFall3 = PhotoImage(file='fall3.png')
    data.blockFall4 = PhotoImage(file='fall4.png')
    data.hintImage = PhotoImage(file='hintTile.png')
    data.backGround = PhotoImage(file='background2.png')
    data.hint = [(-1,-1),(-1,-1)]
    data.blockRow, data.blockCol = data.curLevel['start']
    initSolution(data)
    data.tiles = []
    initTiles(data)
    data.divide = False
    data.gameOver = False
    data.showHint = False
    data.winCount = 0
    data.dy = [0,0,0,0,0]

    
def initSolveByItself(data):
    try:
        data.moveByItself = False
        if ('softBridge' not in data.curLevel 
            and 'hardBridge' not in data.curLevel
            and 'dividedPosition' not in data.curLevel):
            data.solution = getSolution(data, data.curBoard) + [finalStep(data)]
        data.solNum = 0
        data.counter = 0
    except:
        data.solution = None
        data.moveByItself = False
        data.solNum = 0
        data.counter = 0

def finalStep(data):
    return [data.curLevel['target'], data.curLevel['target']]

def nextLevel(data):
    data.curLevel = data.levels[data.levelNum]
    data.curBoard = data.curLevel['board']
    initSolution(data)
    data.step = 0
    data.hint = [(-1,-1),(-1,-1)]
    data.blockRow, data.blockCol = data.curLevel['start']
    data.blockNum = 1
    data.tiles = []
    initTiles(data)
    data.divide = False
    data.gameOver = False
    data.showHint = False
    if ('softBridge' not in data.curLevel 
        and 'hardBridge' not in data.curLevel
        and 'dividedPosition' not in data.curLevel):
        initSolveByItself(data)
    data.winCount = 0
    data.dy = [0,0,0,0,0]

### instruction
def instructionRedrawAll(canvas, data):
    if data.imageNum == 0:
        canvas.create_image(data.width/2, data.height/2, 
            image=data.instructionImage1)
    if data.imageNum == 1:
        canvas.create_image(data.width/2, data.height/2, 
            image=data.instructionImage2)
        

def instructionKeyPressed(event, data):
    if event.keysym == 'space':
        data.imageNum += 1
    if data.imageNum >= 2:
        data.mode = 'playGame'
        data.imageNum = 0
        
        
    
def instructionInit(data):
    data.imageNum = 0
    data.instructionImage1 = PhotoImage(file='instruction.png')
    data.instructionImage2 = PhotoImage(file='instruction32.png')
    data.instructionImage3 = PhotoImage(file='instruction2.png')
    
    
### designInstruction
def designInstructionRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, 
        image=data.instructionImage3)
    
def designInstructionKeyPressed(event, data):
    if event.keysym == 'space':
        data.mode = 'design'
    

### startingSplash mode ###
def startingRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.backGround)
    canvas.create_text(data.width/2, data.height/2-100, 
        text='Bloxorz & Solver & Design', 
        fill='yellow', font='Helvetica 30 italic')
    drawButton(canvas, data)
    
        
def startingMousePressed(event, data):
    gridHeight = 20
    gridWidth = 100
    if (data.width/2-gridWidth <= event.x <= data.width/2+gridWidth and
        data.height/2+50-gridHeight <= event.y <= data.height/2+50+gridHeight):
        data.mode = 'instruction'
    if (data.width/2-gridWidth <= event.x <= data.width/2+gridWidth and
        data.height/2+100-gridHeight <= event.y <= data.height/2+100+gridHeight):
        data.mode = 'levelDisplay'
    if (data.width/2-gridWidth <= event.x <= data.width/2+gridWidth and 
        data.height/2+150-gridHeight <= event.y <= data.height/2+150+gridHeight):
        data.mode = 'designInstruction'
    
def drawButton(canvas, data):
    gridHeight = 20
    gridWidth = 100
    canvas.create_rectangle(data.width/2-gridWidth, data.height/2+50-gridHeight,
        data.width/2+gridWidth, data.height/2+50+gridHeight, fill='yellow')
    canvas.create_text(data.width/2, data.height/2+50, 
        text='New Game', fill='red')
    canvas.create_rectangle(data.width/2-gridWidth, data.height/2+100-gridHeight,
        data.width/2+gridWidth, data.height/2+100+gridHeight, fill='yellow')
    canvas.create_text(data.width/2, data.height/2+100, 
        text='Load Level', fill='red')
    canvas.create_rectangle(data.width/2-gridWidth, data.height/2+150-gridHeight,
        data.width/2+gridWidth, data.height/2+150+gridHeight, fill='yellow')
    canvas.create_text(data.width/2, data.height/2+150, 
        text='Design Board', fill='red')
        
        
### levelDisplay

def levelDisplayRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.backGround)
    canvas.create_text(data.width/2, 30, text='Load Level', 
        fill='yellow', font='Helvetica 26')
    drawLevelList(canvas, data)
    
def drawLevelList(canvas, data):
    num = len(data.levels)
    for i in range(num):
        x0 = (i+1) * (60+50)
        x1 = x0+60
        y0 = 100
        y1 = 160
        canvas.create_rectangle(x0,y0,x1,y1, fill='yellow')
        text = 'Level %d' % (i+1)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text=text, fill='red')
        
def levelDisplayMousePressed(event, data):
    num = len(data.levels)
    for i in range(num):
        if mouseIn(i, event.x, event.y):
            data.levelNum = i
            nextLevel(data)
            data.mode = 'playGame'
            
def levelDisplayKeyPressed(event, data):
    if event.keysym == 'r':
        data.mode = 'startingSplash'

def mouseIn(i, x, y):
    x0 = (i+1) * (60+50)
    x1 = x0+60
    y0 = 100
    y1 = 160
    return (x >= x0 and x <= x1 and y >= y0 and y <= y1)


        
### midSplash

def midSplashRedrawAll(canvas, data):
    text = 'You Won with %d Steps!' % data.step
    canvas.create_text(data.width/2, data.height/2, text=text, 
        fill='yellow', font='Helvetica 18')
    msg1 = 'Press Space to Next Level.'
    msg2 = 'Press t to Replay This Level.\n Press y Back to Home Page'
    canvas.create_text(data.width/2, data.height/2+30, text=msg1, 
        fill='yellow', font='Helvetica 15')
    canvas.create_text(data.width/2, data.height/2+60, text=msg2, 
        fill='yellow', font='Helvetica 15')
        
def midSplashKeyPressed(event, data):
    if event.keysym == 'space':
        data.levelNum = (data.levelNum + 1)%len(data.levels)
        data.mode = 'playGame'
    if event.keysym == 't':
        data.levelNum += 0
        data.mode = 'playGame'
    if event.keysym == 'y':
        data.mode = 'startingSplash'
    if data.levelNum < len(data.levels):
        nextLevel(data)
    
        

### Design mode
# cited from  grid-demo in lecture notes
def designInit(data):
    data.designRows = 15
    data.designCols = 15
    data.designMargin = 50
    data.newBoard = [[0]*data.designCols for row in range(data.designRows)]
    data.part = 1
    data.newLevel = {}
    data.boardWidth = 3/4 * data.width
    data.endTile = PhotoImage(file='end.png')
    data.softSwitch = PhotoImage(file='switch1.png')
    data.hardSwitch = PhotoImage(file='switch2.png')
    data.weakTile = PhotoImage(file='tile2.png')
    data.divider = PhotoImage(file='divider.png')
    data.buildSoftBridge = False
    data.bridgeSoftNum = 0
    data.buildHardBridge = False
    data.bridgeHardNum = 0
    data.buildDivider = False
    data.dividerNum = 0




def designKeyPressed(event, data):
    if event.keysym == 'c':
        designInit(data)
    if event.keysym == 'r':
        data.mode = 'startingSplash'
    if data.buildDivider: data.buildDivider = False; data.dividerNum += 1
    if data.buildSoftBridge: 
        data.buildSoftBridge = False; data.bridgeSoftNum += 1
    if data.buildHardBridge: 
        data.buildHardBridge = False; data.bridgeHardNum += 1
    if event.keysym == 'space':
        data.newLevel['board'] = copy.deepcopy(data.newBoard)
        data.levels.append(copy.deepcopy(data.newLevel))
        designInit(data)
    if event.keysym == 't':
        data.part = 1
    if event.keysym == 's':
        data.part = 0
    if event.keysym == 'e': # end
        data.part = -1
    if event.keysym == 'o': # weak tile
        data.part = 4
    if event.keysym == '1': # soft switch
        if data.bridgeSoftNum == 0: data.part = 2
        else: data.part = 1
    if event.keysym == '2': # hard switch
        if data.bridgeHardNum == 0: data.part = 3
        else: data.part = 1
    if event.keysym == 'd':
        if data.dividerNum == 0: data.part = 5
        else: data.part = 1
    

    
def designMousePressed(event, data):
    if pointInGrid(event.x, event.y, data):
        (row, col) = getCell(event.x, event.y, data)
        if data.part == 0:
            data.newBoard[row][col] = 1
            data.newLevel['start'] = (row, col)
        if data.part == -1:
            data.newBoard[row][col] = data.part
            data.newLevel['target'] = (row, col)
        if data.part == 5 and not data.buildDivider:
            data.newBoard[row][col] = data.part
            data.buildDivider = True
        elif data.part == 5 and data.buildDivider:
            if 'dividedPosition' not in data.newLevel:
                data.newLevel['dividedPosition'] = []
            if data.dividerNum >= len(data.newLevel['dividedPosition']):
                data.newLevel['dividedPosition'].append([])
            (data.newLevel['dividedPosition'][data.dividerNum].append
                (getCell(event.x, event.y, data)))
        elif data.part == 2 and not data.buildSoftBridge:
            data.newBoard[row][col] = data.part
            data.buildSoftBridge = True
        elif data.part == 2 and data.buildSoftBridge:
            if 'softBridge' not in data.newLevel:
                data.newLevel['softBridge'] = []
            if data.bridgeSoftNum >= len(data.newLevel['softBridge']):
                data.newLevel['softBridge'].append([])
            (data.newLevel['softBridge'][data.bridgeSoftNum].append
                (getCell(event.x, event.y, data)))
        elif data.part == 3 and not data.buildHardBridge:
            data.newBoard[row][col] = data.part
            data.buildHardBridge = True
        elif data.part == 3 and data.buildHardBridge:
            if 'hardBridge' not in data.newLevel:
                data.newLevel['hardBridge'] = []
            if data.bridgeHardNum >= len(data.newLevel['hardBridge']):
                data.newLevel['hardBridge'].append([])
            (data.newLevel['hardBridge'][data.bridgeHardNum].append
                (getCell(event.x, event.y, data)))
        elif data.part == 4 or data.part == 1:
            if data.newBoard[row][col] == 0:
                data.newBoard[row][col] = data.part
            else:
                data.newBoard[row][col] = 0


        
def designRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height, fill='wheat')
    canvas.create_text(data.boardWidth/2, 20, 
        text='Design Board!', font='Helvetica 20')
    drawGrids(canvas, data)
    drawElements(canvas, data)
    

    
def drawElements(canvas, data):
    for row in range(6):
        if row == 0: image = data.image; text = 'Press t'; fill='grey'
        if row == 1: image = data.endTile; text = 'Press e'; fill='red'
        if row == 2: image = data.softSwitch; text = 'Press 1'; fill='yellow'
        if row == 3: image = data.hardSwitch; text = 'Press 2'; fill='brown'
        if row == 4: image = data.divider; text = 'Press d'; fill='blue'
        if row == 5: image = data.weakTile; text = 'Press o'; fill='orange'
        canvas.create_image(data.boardWidth+20, 50*(row+1), image=image)
        canvas.create_text(data.boardWidth+70, 50*(row+1), text=text, 
            fill=fill,font='Helvetica 10')
        canvas.create_text(data.boardWidth+70, 350, 
            text='Press s for starting point!', 
            fill='green', font='Helvetica 10')
        
    
# cited from grid-demo
def getCell(x, y, data):
    gridWidth  = data.boardWidth - 2*data.designMargin
    gridHeight = data.height - 2*data.designMargin
    cellWidth  = gridWidth / data.designCols
    cellHeight = gridHeight / data.designRows
    row = (y - data.designMargin) // cellHeight
    col = (x - data.designMargin) // cellWidth
    row = min(data.designRows-1, max(0, row))
    col = min(data.designCols-1, max(0, col))
    return (int(row), int(col))

# cited from grid-demo
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.designMargin <= x <= data.boardWidth-data.designMargin) and
            (data.designMargin <= y <= data.height-data.designMargin))
            
# cited from grid-demo
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.boardWidth - 2*data.designMargin
    gridHeight = data.height - 2*data.designMargin
    columnWidth = gridWidth / data.designCols
    rowHeight = gridHeight / data.designRows
    x0 = data.designMargin + col * columnWidth
    x1 = data.designMargin + (col+1) * columnWidth
    y0 = data.designMargin + row * rowHeight
    y1 = data.designMargin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

def drawGrids(canvas, data):
    # draw grid of cells
    for row in range(data.designRows):
        for col in range(data.designCols):
            text = ''
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = getFill(row, col, data)
            if ('softBridge' in data.newLevel and 
                data.bridgeSoftNum < len(data.newLevel['softBridge']) and
                (row, col) in data.newLevel['softBridge'][data.bridgeSoftNum]):
                fill = 'yellow'
                text = str(data.bridgeSoftNum)
            if ('hardBridge' in data.newLevel and 
                data.bridgeHardNum < len(data.newLevel['hardBridge']) and
                (row, col) in data.newLevel['hardBridge'][data.bridgeHardNum]):
                fill = 'brown'
                text = str(data.bridgeHardNum)
            if ('dividedPosition' in data.newLevel and 
                data.dividerNum < len(data.newLevel['dividedPosition']) and
                (row, col) in data.newLevel['dividedPosition'][data.dividerNum]):
                fill = 'blue'
                text = str(data.dividerNum)
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text=text)
    
def getFill(row, col, data):
    if 'start' in data.newLevel and (row, col)==data.newLevel['start']:
        return 'green'
    if 'target' in data.newLevel and (row, col)==data.newLevel['target']:
        return 'red'
    elif data.newBoard[row][col] == 0:
        return 'white'
    if data.newBoard[row][col] == 1:
        return 'grey'
    if data.newBoard[row][col] == 4:
        return 'orange'
    if data.newBoard[row][col] == 2:
        return 'yellow'
    if data.newBoard[row][col] == 3:
        return 'brown'
    if data.newBoard[row][col] == 5:
        return 'blue'



### playGame mode ###
def initTiles(data):
    newBoard = convertRowCol(data.curBoard)
    rows, cols = len(newBoard), len(newBoard[0])
    data.tiles = [[0] * cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if newBoard[row][col] == 1: 
                data.tiles[row][col] = PhotoImage(file="tile1.png")
            if newBoard[row][col] == -1:
                data.tiles[row][col] = PhotoImage(file='end.png')
            if newBoard[row][col] == 2:
                data.tiles[row][col] = PhotoImage(file='switch1.png')
            if newBoard[row][col] == 3:
                data.tiles[row][col] = PhotoImage(file='switch2.png')
            if newBoard[row][col] == 4:
                data.tiles[row][col] = PhotoImage(file='tile2.png')
            if newBoard[row][col] == 5:
                data.tiles[row][col] = PhotoImage(file='divider.png')
                
def convertRowCol(L):
    rows, cols = len(L), len(L[0])
    result = [[0]*rows for col in range(cols)]
    for newRow in range(cols):
        for newCol in range(rows):
            result[newRow][newCol] = L[newCol][newRow]
    return result
            
            
def drawBlock(data, canvas):
    row = data.blockCol # switch row and col owing to the way tiles are arranged
    col = data.blockRow
    dy = data.dy[0]
    if data.blockNum == 0:
        drow1, dcol1 = data.dblockCol1, data.dblockRow1
        drow2, dcol2 = data.dblockCol2, data.dblockRow2
        canvas.create_image(data.width/3+32*drow1+10*dcol1-77, 
            data.height/3-5*drow1+16*dcol1+43+dy, image=data.dBlockImage)
        canvas.create_image(data.width/3+32*drow2+10*dcol2-77, 
            data.height/3-5*drow2+16*dcol2+43+dy, image=data.dBlockImage)
    if checkWin(data):
        if data.winCount == 0:
            canvas.create_image(data.width/3+32*row+10*col-77, 
                data.height/3-5*row+16*col+30, image=data.blockFall1)
        if data.winCount == 1:
            canvas.create_image(data.width/3+32*row+10*col-77, 
                data.height/3-5*row+16*col+43, image=data.blockFall3)
        if data.winCount == 2:
            canvas.create_image(data.width/3+32*row+10*col-77, 
                data.height/3-5*row+16*col+50, image=data.blockFall4)
        return 
    if data.blockNum == 1:
        canvas.create_image(data.width/3+32*row+10*col-77, 
            data.height/3-5*row+16*col+30+dy, image=data.blockImage)
    if data.blockNum == 2:
        canvas.create_image(data.width/3+32*row+10*(col+1)-77, 
            data.height/3-5*row+16*(col+1)+30+dy, image=data.blockImage2)
    if data.blockNum == 3:
        canvas.create_image(data.width/3+32*row+10*col-77, 
            data.height/3-5*row+16*col+30+dy, image=data.blockImage3)

        
def fallingTiles(data):
    for i in range(len(data.dy)):
        if data.dy[i] < data.height: 
            data.dy[i] += random.randint(50, 150)
    # when game over, tiles falling down
    
            
def drawTiles(data, canvas):
    for row in range(len(data.tiles)-1, -1, -1):
        for col in range(len(data.tiles[row])):
            dy = random.choice(data.dy)
            if data.hint == None and data.tiles[row][col] == 0: continue
            if data.hint == None and data.tiles[row][col] != 0: 
                curImage = data.tiles[row][col]
            elif (row, col) == data.hint[0] or (row, col) == data.hint[1]:
                curImage = data.hintImage
            elif data.tiles[row][col] != 0:
                curImage = data.tiles[row][col]
            else: continue
            canvas.create_image(data.width/3+32*row+10*col-77, 
                data.height/3-5*row+16*col+62+dy, image=curImage)



def convert(L):
    # l is in the form of [(a,b),(c,d)] needs to return [(b,a),(d,c)]
    newL1, newL2 = [0,0], [0,0]
    if L == None: return
    for i in range(len(L)):
        for j in range(len(L[i])):
            if i == 0: newL1[1-j] = L[i][j]
            elif i == 1: newL2[1-j] = L[i][j]
    return [tuple(newL1), tuple(newL2)]
            

def playGameKeyPressed(event, data):
    if event.keysym == 'a':
        nextLevel(data)
    if event.keysym == 'r':
        nextLevel(data)
        data.mode = 'startingSplash'
    if data.gameOver: return None
    if (event.keysym == 'h'):
        data.hint = convert(showHint(data, data.curBoard))
    if (event.keysym == 'q'):
        data.moveByItself = True
    if (event.keysym == 'Up' or event.keysym == 'Down' 
        or event.keysym == 'Left' or event.keysym == 'Right'):
        data.hint = [(-1,-1),(-1,-1)]
        data.step += 1
    moveBlock(event, data)
    changeBoard(data)
    divideBlock(event, data)
    if data.divide and neighbor(data):
        data.divide = False
        combine(data)
        

        
def getSolution(data, board):
    row1, col1, row2, col2 = getRowCol(data)
    solution = solver2(board, data.blockNum, row1, col1, row2, col2, 
        data.curLevel['target'])
    return solution



        
def showHint(data, board):
    next = nextStep(board, data)
    if next != None:
        hrow1,hcol1,hrow2,hcol2 = next
        return [(hrow1, hcol1), (hrow2, hcol2)]
        
def nextStep(board, data):
    if ('softBridge' in data.curLevel or 'hardBridge' in data.curLevel
        or 'dividePosition' in data.curLevel): return None
    row1, col1, row2, col2 = getRowCol(data)
    result = solver2(board, data.blockNum, row1, col1, row2, col2, 
        data.curLevel['target'])
    if result == None: return
    if len(result) > 1:
        return tuple(list(result[1][0]) + list(result[1][1]))

    
# Solver!
def isLegalInSolver(board, row1, col1, row2, col2):
    rows, cols = len(board), len(board[0])
    if (row1 < 0 or row1 >= rows or row2 < 0 or row2 >= rows or
        col1 < 0 or col1 >= cols or col2 < 0 or col2 >= cols):
        return False
    if board[row1][col1] == 0 or board[row2][col2] == 0:
        return False
    return True

            
def solver2(board, blockNum, row1, col1, row2, col2, target, constraint=[], shortest=[]):
    if not isLegalInSolver(board, row1, col1, row2, col2): return
    coord = sorted([(row1, col1), (row2, col2)])
    (row1, col1) = coord[0]
    (row2, col2) = coord[1]
    if coord in constraint: return
    if (row1, col1) == target and blockNum == 1: return constraint
    newConstraints = constraint + [coord]
    if shortest != [] and len(newConstraints) >= len(shortest): return
    if blockNum == 1:
        if board[row1][col1] == 4: return
        a = solver2(board, 2, row1-1, col1, row2-2, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 2, row1+1, col1, row2+2, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 3, row1, col1-2, row2, col2-1, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 3, row1, col1+2, row2, col2+1, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
    if blockNum == 3:
        a = solver2(board, 3, row1-1, col1, row2-1, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 3, row1+1, col1, row2+1, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 1, row1, col1-1, row2, col2-2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 1, row1, col1+2, row2, col2+1, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
    if blockNum == 2:
        a = solver2(board, 1, row1-1, col1, row2-2, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 1, row1+2, col1, row2+1, col2, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 2, row1, col1-1, row2, col2-1, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
        a = solver2(board, 2, row1, col1+1, row2, col2+1, target, newConstraints, shortest)
        if a != None and (shortest == [] or len(a) < len(shortest)): 
            shortest = a
    if shortest == []:
        return 
    else:
        return shortest

        

def getRowCol(data):
    if data.blockNum == 1:
        return (data.blockRow, data.blockCol, data.blockRow, data.blockCol)
    elif data.blockNum == 2:
        return (data.blockRow, data.blockCol, data.blockRow+1, data.blockCol)
    elif data.blockNum == 3:
        return (data.blockRow, data.blockCol, data.blockRow, data.blockCol+1)
        
        
        

# divider
def divideBlock(event, data):
    if not isLegal(data): return
    # divide
    if (data.curBoard[data.blockRow][data.blockCol] == 5) and (not data.divide): 
        data.blockNum = 0 # no such 1x2 block anymore
        data.controlBlock1 = True
        data.divide = True
        data.dblockRow1, data.dblockCol1 = data.curLevel['dividedPosition'][0][0]
        data.dblockRow2, data.dblockCol2 = data.curLevel['dividedPosition'][0][1]

            
def neighbor(data):
    if abs(data.dblockRow1-data.dblockRow2)==1 and (data.dblockCol1==data.dblockCol2):
        return True
    if abs(data.dblockCol1-data.dblockCol2)==1 and (data.dblockRow1==data.dblockRow2):
        return True
        
def combine(data):
    if (data.dblockRow1 < data.dblockRow2) and (data.dblockCol1==data.dblockCol2):
        data.blockNum = 2
        data.blockRow, data.blockCol = data.dblockRow1, data.dblockCol1
    elif (data.dblockRow1 > data.dblockRow2) and (data.dblockCol1==data.dblockCol2):
        data.blockNum = 2
        data.blockRow, data.blockCol = data.dblockRow2, data.dblockCol2
    if (data.dblockCol1 < data.dblockCol2) and (data.dblockRow1 == data.dblockRow2):
        data.blockNum = 3
        data.blockRow, data.blockCol = data.dblockRow1, data.dblockCol1
    elif (data.dblockCol1 > data.dblockCol2) and (data.dblockRow1 == data.dblockRow2):
        data.blockNum = 3
        data.blockRow, data.blockCol = data.dblockRow2, data.dblockCol2
    
    
# soft/hard switch
def changeBoard(data):
    if not isLegal(data): return
    if data.blockNum == 1:
        if (data.curBoard[data.blockRow][data.blockCol] == 2):
            changeSoftBridge(data)
        elif (data.curBoard[data.blockRow][data.blockCol] == 3):
            changeHardBridge(data)
    elif data.blockNum == 2:
        if (data.curBoard[data.blockRow][data.blockCol] == 2 or (data.blockRow+1>=0 and
            data.blockRow+1<len(data.curBoard) and 
            data.curBoard[data.blockRow+1][data.blockCol] == 2)):
            changeSoftBridge(data)
    elif data.blockNum == 3:
        if (data.curBoard[data.blockRow][data.blockCol] == 2 or 
            (data.blockCol+1 < len(data.curBoard[0]) and
            data.curBoard[data.blockRow][data.blockCol] == 2)):
            changeSoftBridge(data)
            
            
def changeSoftBridge(data):
    for bridge in data.curLevel['softBridge']:
        for position in bridge:
            row, col = position
            if data.curBoard[row][col] == 0:
                data.curBoard[row][col] = 1
                data.tiles[col][row] = PhotoImage(file='tile1.png')
            elif data.curBoard[row][col] == 1:
                data.curBoard[row][col] = 0
                data.tiles[col][row] = 0
            
def changeHardBridge(data):
    for bridge in data.curLevel['hardBridge']:
        for position in bridge:
            row, col = position
            if data.curBoard[row][col] == 0:
                data.curBoard[row][col] = 1
                data.tiles[col][row] = PhotoImage(file='tile1.png')
            elif data.curBoard[row][col] == 1:
                data.curBoard[row][col] = 0
                data.tiles[col][row] = 0
        
    
def isLegal(data):
    rows, cols = len(data.curBoard), len(data.curBoard[0])
    if data.divide == True:
        return ((data.dblockRow1 >= 0 and data.dblockRow1 < rows and 
            data.dblockCol1 >= 0 and data.dblockCol1 < cols) and 
            (data.dblockRow2 >= 0 and data.dblockRow2 < rows and 
            data.dblockCol2 >= 0 and data.dblockCol2 < cols) and
            data.curBoard[data.dblockRow1][data.dblockCol1] != 0
            and data.curBoard[data.dblockRow2][data.dblockCol2] != 0)
    if data.blockNum == 1:
        if (data.blockRow < 0 or data.blockRow >= rows or data.blockCol < 0
            or data.blockCol >= cols):
            
            return False
        if (data.curBoard[data.blockRow][data.blockCol] == 0 or 
            data.curBoard[data.blockRow][data.blockCol] == 4):
            return False
    elif data.blockNum == 2:
        if (data.blockRow < 0 or data.blockRow+1 >= rows or data.blockCol < 0
            or data.blockCol >= cols):
            return False
        if (data.curBoard[data.blockRow][data.blockCol] == 0 or 
            data.curBoard[data.blockRow+1][data.blockCol] == 0):
            return False
    elif data.blockNum == 3:
        if (data.blockRow < 0 or data.blockRow >= rows or data.blockCol < 0
            or data.blockCol+1 >= cols):
            return False
        if (data.curBoard[data.blockRow][data.blockCol] == 0 or
            data.curBoard[data.blockRow][data.blockCol+1] == 0):
            return False
    return True
            
# move block
def moveDividedBlock(event, data):
    if data.controlBlock1 == True:
        if event.keysym == 'Left':
            data.dblockCol1 -= 1
        if event.keysym == 'Right':
            data.dblockCol1 += 1
        if event.keysym == 'Up':
            data.dblockRow1 -= 1
        if event.keysym == 'Down':
            data.dblockRow1 += 1
    else:
        if event.keysym == 'Left':
            data.dblockCol2 -= 1
        if event.keysym == 'Right':
            data.dblockCol2 += 1
        if event.keysym == 'Up':
            data.dblockRow2 -= 1
        if event.keysym == 'Down':
            data.dblockRow2 += 1
            
def moveBlockNum1(event, data):
    if event.keysym == 'Left':
        data.blockCol -= 2
        data.blockNum = 3
    if event.keysym == 'Right':
        data.blockCol += 1
        data.blockNum = 3
    if event.keysym == 'Up':
        data.blockRow -= 2
        data.blockNum = 2
    if event.keysym == 'Down':
        data.blockRow += 1
        data.blockNum = 2

def moveBlockNum2(event, data):
    if event.keysym == 'Left':
        data.blockCol -= 1
    if event.keysym == 'Right':
        data.blockCol += 1
    if event.keysym == 'Up':
        data.blockRow -= 1
        data.blockNum = 1
    if event.keysym == 'Down':
        data.blockRow += 2
        data.blockNum = 1
        
def moveBlockNum3(event, data):
    if event.keysym == 'Left':
        data.blockCol -= 1
        data.blockNum = 1
    if event.keysym == 'Right':
        data.blockCol += 2
        data.blockNum = 1
    if event.keysym == 'Up':
        data.blockRow -= 1
    if event.keysym == 'Down':
        data.blockRow += 1
    
def moveBlock(event, data):
    if data.blockNum == 0:
        if event.keysym == 'space':
            data.controlBlock1 = not data.controlBlock1
        moveDividedBlock(event, data)
    if data.blockNum == 1:
        moveBlockNum1(event, data)
    elif data.blockNum == 2:
        moveBlockNum2(event, data)
    elif data.blockNum == 3:
        moveBlockNum3(event, data)
    if not isLegal(data): data.gameOver = True


def updateBlock(data):
    if data.solution == None or data.solNum >= len(data.solution): return
    curSolPos = data.solution[data.solNum]
    data.blockRow, data.blockCol = curSolPos[0]
    data.blockNum = getBlockNum(curSolPos[0][0], curSolPos[0][1], 
        curSolPos[1][0], curSolPos[1][1])
    data.solNum += 1
    data.step += 1
    
def getBlockNum(row1, col1, row2, col2):
    if row1 == row2 and col1 == col2: return 1
    if row1 == row2-1 and col1 == col2: return 2
    if row1 == row2 and col1 == col2-1: return 3

def timerFired(data):
    if data.counter % 5 == 0 and data.moveByItself:
        updateBlock(data)
    if data.winCount >= 3 and checkWin(data):
        data.mode = 'midSplash'
    if checkWin(data):
        data.moveByItself = False
        data.winCount += 1
    if data.gameOver:
        fallingTiles(data)


def checkWin(data):
    rows, cols = len(data.curBoard), len(data.curBoard[0])
    if (data.blockNum == 1 and 0 <= data.blockRow < rows 
        and 0 <= data.blockCol < cols):
        return data.curBoard[data.blockRow][data.blockCol] == -1

def playGameRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.backGround)
    drawTiles(data, canvas)
    drawBlock(data, canvas)
    canvas.create_text(data.width-80, 40, text='Steps: '+str(data.step),
        font='Helvetica 18', fill='yellow')
    if data.gameOver:
        canvas.create_text(data.width/2, data.height/2, text='Game Over\nPress a to replay', font='Helvetica 26 bold', fill='yellow')
        
###### wraper
def mousePressed(event, data):
    if data.mode == 'design': designMousePressed(event, data)
    if data.mode == 'levelDisplay': levelDisplayMousePressed(event, data)
    if data.mode == 'startingSplash': startingMousePressed(event, data)
    

def keyPressed(event, data):
    if data.mode == 'playGame':
        playGameKeyPressed(event, data)
    if data.mode == 'levelDisplay':
        levelDisplayKeyPressed(event, data)
    if data.mode == 'design':
        designKeyPressed(event, data)
    if data.mode == 'midSplash':
        midSplashKeyPressed(event, data)
    if data.mode == 'instruction':
        instructionKeyPressed(event, data)
    if data.mode == 'designInstruction':
        designInstructionKeyPressed(event, data)


def redrawAll(canvas, data):
    if data.mode == 'startingSplash':
        startingRedrawAll(canvas, data)
    if data.mode == 'instruction':
        instructionRedrawAll(canvas, data)
    if data.mode == 'designInstruction':
        designInstructionRedrawAll(canvas, data)
    if data.mode == 'levelDisplay':
        levelDisplayRedrawAll(canvas, data)
    if data.mode == 'playGame':
        playGameRedrawAll(canvas, data)
    if data.mode == 'midSplash':
        playGameRedrawAll(canvas, data)
        midSplashRedrawAll(canvas, data)
    if data.mode == 'design':
        designRedrawAll(canvas, data)




####################################
####################################
# use the run function as-is
####################################
####################################
# cited from example0 in lecture notes
def run(width=700, height=533):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    
    root = Tk()
    init(data)
    # create the root and the canvas

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 533)
