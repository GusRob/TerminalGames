import math
import time
import random
import time
import pygame
import curses
import os.path
from curses import wrapper
from collections import Counter

# ████████╗███████╗████████╗██████╗ ██╗███████╗
# ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝
#    ██║   █████╗     ██║   ██████╔╝██║███████╗
#    ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║
#    ██║   ███████╗   ██║   ██║  ██║██║███████║
#    ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝


   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line block game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Piece:
    pieces = [
    [[4, 5, 6, 7], [1, 5, 9, 13]],  #I Shape
    [[4, 5, 9, 10], [2, 6, 5, 9]],  #Z Shape
    [[6, 7, 9, 10], [1, 5, 6, 10]], #S Shape
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  #J Shape
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],    #L Shape
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],   #T Shape
    [[1, 2, 5, 6]], #O Shape
    ]
    def __init__(self, initX, initY, board):
        self.pos = [initX,initY]
        self.type = random.randint(0,6)
        self.board = board
        self.rotation = 0
    def cells(self):
        result = []
        for i in range(4):
            val = self.pieces[self.type][self.rotation][i]
            result.append([self.pos[0] + val%4 , self.pos[1] + int(val/4)])
        return result
    def rotate(self):
        canRotate = self.checkIntersect([self.pos[0], self.pos[1]], (self.rotation+1)%len(self.pieces[self.type]), self.type)
        if canRotate :
            self.rotation = (self.rotation+1)%len(self.pieces[self.type])
        return
        return
    def move(self, direction):
        canMove = self.checkIntersect([self.pos[0] + direction, self.pos[1]], self.rotation, self.type)
        if canMove :
            self.pos[0] += direction
        return
    def drop(self):
        canDrop = self.checkIntersect([self.pos[0], self.pos[1]+1], self.rotation, self.type)
        if canDrop :
            self.pos[1] += 1
        else:
            self.addPieceToBoard()
        return
    def addPieceToBoard(self):
        for i in range(4):
            val = self.pieces[self.type][self.rotation][i]
            coords = [self.pos[0] + val%4 , self.pos[1] + int(val/4)]
            self.board.state[coords[1]][coords[0]] = self.type+1
        self.board.piece = self.board.newPiece()
        self.board.update()
        return
    def checkIntersect(self, newPos, newRot, newType):
        isValid = True
        for i in range(4):
            val = self.pieces[newType][newRot][i]
            coords = [newPos[0] + val%4 , newPos[1] + int(val/4)]
            if(coords[0] > -1 and coords[0] < len(self.board.state[0]) and coords[1] > -1 and coords[1] < len(self.board.state)):
                if(self.board.state[coords[1]][coords[0]] != 0):
                    isValid = False
            else:
                isValid = False
        return isValid

class Board:
    def __init__(self):
        self.state = [[0 for i in range(7)] for j in range(25)]
        self.gameOver = False
        self.moveCounter = 0
        self.piece = self.newPiece()
        self.speed = 10
        self.score = 0
        self.newHigh = False
        self.next = 0
        self.saved = 0
    def newPiece(self):
        return Piece(0,0,self)
    def deleteRow(self):
        return
    def update(self):
        return
    def __str__(self, stdscr):
        nextWin = ["╔════════╗", "║        ║","║        ║","║        ║","╚════════╝", "", "","","", "","", "", "","","", "","", "","", "","","", "", " Held:", "╔════════╗","║        ║","║        ║", "║        ║"]
        stdscr.addstr("╔════════════════╗ Next:\n")
        for i in range(len(self.state)):
            stdscr.addstr("║ ")
            for j in range(len(self.state[0])):
                val = self.state[i][j]
                if val != 0:
                    stdscr.addstr('██', curses.color_pair(val))
                else:
                    if([j,i] in self.piece.cells()):
                        stdscr.addstr('██', curses.color_pair(self.piece.type+1))
                    else:
                        col = 7 if i == 3 else 3
                        stdscr.addstr('⤙⤚', curses.color_pair(col))#'░░''⇃↾''⤙⤚''⟶⟵'
            addition = nextWin[i]
            stdscr.addstr(" ║" + addition + "\n")
        stdscr.addstr("╚════════════════╝╚════════╝\n")

        return

random.seed()
stdscr = curses.initscr() #initialise curses
curses.noecho()             #turn off echoing of keys to screen
curses.cbreak()              #allow game to react to key presses without waiting for return key
stdscr.keypad(True)         #cause special keys to be returned in curses format
stdscr.nodelay(True)         #game doesnt wait for user to press a key

def readHScore():
    result = [-1]
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        result = lines[2][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[2][1] = score
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                lines[i][j] = str(lines[i][j])
        result = []
        for i in range(len(lines)):
            result.append(" ".join(lines[i]))
        output = "\n".join(result)
        with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "w") as textFile:
            textFile.write(output)
    return score

def gameLoop(stdscr, info, key, keys, object, pause, hScore):
    stdscr.clear()
    key = stdscr.getch()

    if pause and key != -1 and not object.gameOver:
        pause = False

    if(key == curses.KEY_UP and (not pause)):
        object.piece.rotate()
    elif(key == curses.KEY_DOWN and (not pause)):
        object.piece.drop()
    elif(key == curses.KEY_LEFT and (not pause)):
        object.piece.move(-1)
    elif(key == curses.KEY_RIGHT and (not pause)):
        object.piece.move(1)
    elif(key == ord('r')):
        object = Board()
        pause = True
    elif(key == ord('i')):
        newWalls = not object.solidWalls
        object = Board()
        object.solidWalls = newWalls
        pause = True

    if not pause:
        object.moveCounter += 1
        if(object.moveCounter >= object.speed):
            object.moveCounter = 0
            object.piece.drop()

    if(object.gameOver):
        pause = True
        object.death-=1

    object.__str__(stdscr)

    if object.score > int(hScore):
        hScore = object.score
        object.newHigh = True

    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    if object.gameOver:
        info.addstr("Game Over!\n\n", curses.A_BLINK)
        if(object.newHigh):
            info.addstr("New High Score!\n\n")
            updateHScore(object.score)
            hScore = readHScore()
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n\n")
    else:
        info.addstr("Instructions:\n")
        info.addstr("Use the Left and Right Keys to move\n")
        info.addstr("Use the Up Key to rotate\n")
        info.addstr("Use the Down Key to drop\n")
        info.addstr("Complete a row for points!\n")
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n\n")
    stdscr.refresh()
    info.refresh()


    time.sleep(0.05)

    return object, pause, hScore, key

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    object = Board()
    rows, cols = stdscr.getmaxyx()
    x = 40
    info = curses.newwin(rows, 35, 0, x)

    pause = True
    keys = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_ENTER, ord('q'), ord('r'), ord('i')]
    key = -1

    while key != ord('q'):
        object, pause, hScore, key = gameLoop(stdscr, info, key, keys, object, pause, hScore)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
