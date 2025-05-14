#################################################
# hw9.py: Tetris!
#
# Your name: Abhi Yadagiri
# Your andrew id: ayadagir
# Section: A
# Your partner's name:
# Your partner's andrew id:
#################################################

import cs112_n22_week4_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + 2 * margin
    height = rows * cellSize + 2 * margin
    return (width, height)

def print2dList(a):
    if (a == []): print([]); return
    rows, cols = len(a), len(a[0])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(str(a[row][col])) for row in range(rows)])
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).ljust(colWidths[col]), end='')
        print(' ]')
    print(']')

def appStarted(app):
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions()
    app.emptyColor = "blue"
    app.board = [[app.emptyColor] * app.cols for row in range(app.rows)]
    app.iPiece = [
        [  True,  True,  True,  True ]
    ]
    app.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    app.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    app.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    app.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    app.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    app.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [app.iPiece, app.jPiece, app.lPiece, app.oPiece, 
                        app.sPiece, app.tPiece, app.zPiece]
    app.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
                             "green", "orange"]
    app.object = (app.board, app.emptyColor, app.tetrisPieces, 
                app.tetrisPieceColors)
    app.fallingPiece = [[]]
    app.fallingPieceColor = None
    app.fallingPieceRow = 0
    app.fallingPieceCol = 0
    newFallingPiece(app)
    app.isPaused = False
    app.isGameOver = False
    app.fullRows = 0
    app.score = 0

def keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
    if not app.isGameOver:
        if event.key == "p":
            app.isPaused = not app.isPaused
        if event.key == "s":
            doStep(app)
        if event.key == "Space":
            moveFallingPiece(app, app.rows, 0)
        if event.key == "Up":
            rotateFallingPiece(app)
        if event.key == "Down":
            moveFallingPiece(app, 1, 0)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, -1, 0)
        if event.key == "Left":
            moveFallingPiece(app, 0, -1)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, 0, 1)
        if event.key == "Right":
            moveFallingPiece(app, 0, 1)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, 0, -1)

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceRow = 0
    app.fallingPieceCol = len(app.board[0]) // 2 - len(app.fallingPiece[0]) // 2

def drawFallingPiece(app, canvas):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col] == True:
                canvas.create_rectangle(app.margin + app.cellSize *
                                       (app.fallingPieceCol + col), 
                                        app.margin + app.cellSize * 
                                       (app.fallingPieceRow + row), 
                                        app.margin + app.cellSize * 
                                       (app.fallingPieceCol + col + 1),
                                        app.margin + app.cellSize * 
                                       (app.fallingPieceRow + row + 1),
                                        fill = app.fallingPieceColor, width = 4)

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if fallingPieceIsLegal:
        return True
    else:
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False

def fallingPieceIsLegal(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col] == True:
                if (app.fallingPieceRow < 0 or app.fallingPieceRow + row 
                    >= app.rows or app.fallingPieceCol < 0 or 
                    app.fallingPieceCol + col >= app.cols):
                    return False
                if app.board[app.fallingPieceRow + row][app.fallingPieceCol 
                             + col] != app.emptyColor:
                    return False
    return True

def rotateFallingPiece(app):
    oldPiece = app.fallingPiece
    oldFallingPieceRow = app.fallingPieceRow
    oldFallingPieceCol = app.fallingPieceCol
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    newRows = oldCols
    newCols = oldRows
    newPiece = [[None] * newCols for row in range(newRows)]
    for row in range(len(oldPiece)):
        for col in range(len(oldPiece[row])):
            newPiece[(oldCols - 1) - col][row] = oldPiece[row][col]
    app.fallingPiece = newPiece
    app.fallingPieceRow = oldFallingPieceRow + oldRows // 2 - newRows // 2
    app.fallingPieceCol = oldFallingPieceCol + oldCols // 2 - newCols // 2
    if not fallingPieceIsLegal(app):
        app.fallingPiece = oldPiece
        app.fallingPieceRow = oldFallingPieceRow
        app.fallingPieceCol = oldFallingPieceCol

def placeFallingPiece(app):
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][col] == True:
                app.board[app.fallingPieceRow + row][app.fallingPieceCol 
                          + col] = app.fallingPieceColor
    removeFullRows(app)

def doStep(app):
    moveFallingPiece(app, 1, 0)

def timerFired(app):
    if not app.isGameOver:
        if not app.isPaused:
            doStep(app)
            if not fallingPieceIsLegal(app):
                moveFallingPiece(app, -1, 0)
                placeFallingPiece(app)
                newFallingPiece(app)
                if not fallingPieceIsLegal(app):
                    app.isGameOver = True

def removeFullRows(app):
    isFullRow = True
    newBoard = [[app.emptyColor] * app.cols for row in range(app.rows)] 
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if app.board[row][col] == app.emptyColor:
                isFullRow = False
            newBoard[row][col] = app.board[row][col]
        if isFullRow:
            app.fullRows += 1
            app.score += app.fullRows ** 2
            newBoard.pop(row)
            newBoard.insert(0, [app.emptyColor] * app.cols)
        isFullRow = True
        app.fullRows = 0
    app.board = newBoard

def drawScore(app, canvas):
    canvas.create_text(app.width / 2, app.margin / 2, 
                       text = f"Score: {app.score}", font = "Arial 10 bold")

def drawCell(app, canvas, row, col):
    canvas.create_rectangle(app.margin + app.cellSize * col, 
                            app.margin + app.cellSize * row, 
                            app.margin + app.cellSize * (col + 1),
                            app.margin + app.cellSize * (row + 1),
                            fill = app.board[row][col], width = 4)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "orange")
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.isGameOver:
        canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, 
                                3 * app.margin, fill = "black")
        canvas.create_text(app.width / 2, 2 * app.margin, text = "GAME OVER!!!",
                           fill = "red", font = "Arial 16 bold")

#################################################
# main
#################################################

def main():
    cs112_n22_week4_linter.lint()
    playTetris()
    runApp(width=playTetris()[0], height=playTetris()[1])

if __name__ == '__main__':
    main()
