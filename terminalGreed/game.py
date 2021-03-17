import math
import time
import random
import curses
import os.path
from curses import wrapper
from collections import Counter

#  ██████╗ ██████╗ ███████╗███████╗██████╗
# ██╔════╝ ██╔══██╗██╔════╝██╔════╝██╔══██╗
# ██║  ███╗██████╔╝█████╗  █████╗  ██║  ██║
# ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║  ██║
# ╚██████╔╝██║  ██║███████╗███████╗██████╔╝
#  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝


   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line logical number game in Python.#
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self, size):
        self.size = size
        self.state = self.generateNums()
        self.score = 0
        self.selected = [0,0]
        self.selecting = True
        self.isGameOver = False
        self.neck = [-1,-1]
    def generateNums(self):
        return[[random.randint(1, 9) for i in range(self.size)] for j in range(self.size)]
    def move(self, direction):
        firstPos = [self.selected[0] + direction[0], self.selected[1] + direction[1]]
        if(max(firstPos) >= self.size or min(firstPos) <= -1):
            fail = True
        else:
            n = self.state[firstPos[1]][firstPos[0]]
            fail = False
        if not fail:
            if n == -1:
                fail = True
        if not fail:
            for i in range(n):
                if not fail:
                    nextPos = [self.selected[0] + direction[0], self.selected[1] + direction[1]]
                    if (max(nextPos) >= self.size or min(nextPos) <= -1) or self.state[nextPos[1]][nextPos[0]] == -1:
                        fail = True
                    else:
                        self.state[self.selected[1]][self.selected[0]] = -1
                        self.neck = self.selected[:]
                        self.selected = nextPos
        if not fail:
            self.score += n
        return fail
    def colOfSq(self, square):
        result = -1
        if(max(square) >= self.size):
            result = -1
        else:
            val = self.state[square[1]][square[0]]
            if(val == -1):
                if(self.isGameOver):
                    result = 1
                else:
                    result = 3
        return result
    def __str__(self, stdscr):
        if(self.isGameOver):
            bodyCol = curses.color_pair(1)
        else:
            bodyCol = curses.color_pair(3)
        stdscr.addstr("╔")
        for i in range(self.size*2+1):
            stdscr.addstr("═")
        stdscr.addstr("╗\n")
        part = 0
        for i in range(self.size):
            stdscr.addstr("║")
            rightCol = self.colOfSq([0,i])
            if rightCol == -1:
                stdscr.addstr(" ", curses.color_pair(1))
            else:
                stdscr.addstr("▐", curses.color_pair(rightCol))
            for j in range(self.size):
                val = self.state[i][j]
                if(self.selected != [j,i]):
                    if(val == -1):
                        stdscr.addstr("█", bodyCol)
                    else:
                        stdscr.addstr(str(val), curses.color_pair(val))
                elif not self.selecting:
                    stdscr.addstr(" ", curses.color_pair(10))
                else:
                    stdscr.addstr(str(val), curses.color_pair(10))
                if(([j,i] == self.selected and [j+1,i] == self.neck) or ([j+1,i] == self.selected and [j,i] == self.neck)):
                    stdscr.addstr("█", bodyCol)
                else:
                    leftCol = self.colOfSq([j,i])
                    rightCol = self.colOfSq([j+1,i])
                    if(rightCol == -1 and leftCol == -1):
                        stdscr.addstr(" ", curses.color_pair(leftCol))
                    elif(rightCol == leftCol):
                        stdscr.addstr("█", curses.color_pair(leftCol))
                    elif(rightCol == -1):
                        stdscr.addstr("▌", curses.color_pair(leftCol))
                    elif(leftCol == -1):
                        stdscr.addstr("▐", curses.color_pair(rightCol))
            stdscr.addstr("║\n")
        stdscr.addstr("╚")
        for i in range(self.size*2+1):
            stdscr.addstr("═")
        stdscr.addstr("╝\n")
        return

def isAnInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

random.seed()
stdscr = curses.initscr() #initialise curses
curses.noecho()             #turn off echoing of keys to screen
curses.cbreak()              #allow game to react to key presses without waiting for return key
stdscr.keypad(True)         #cause special keys to be returned in curses format

def readHScore():
    result = [-1]
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        result = lines[6][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[6][1] = score
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

def gameLoop(stdscr, info, key, keys, object, pause, hScore, boardSize, newHigh):
    while not str(key) in keys:
        key = stdscr.getkey()
    stdscr.clear()

    if(key == "KEY_UP" and not pause):
        if(object.selecting):
            object.selected[1] = object.selected[1]-1
            if object.selected[1] <= -1:
                object.selected[1] = object.size-1
        else:
            pause = object.move([0,-1])
    elif(key == "KEY_DOWN" and not pause):
        if(object.selecting):
            object.selected[1] = object.selected[1]+1
            if object.selected[1] >= object.size:
                object.selected[1] = 0
        else:
            pause = object.move([0,1])
    elif(key == "KEY_LEFT" and not pause):
        if(object.selecting):
            object.selected[0] = object.selected[0]-1
            if object.selected[0] <= -1:
                object.selected[0] = object.size-1
        else:
            pause = object.move([-1,0])
    elif(key == "KEY_RIGHT" and not pause):
        if(object.selecting):
            object.selected[0] = object.selected[0]+1
            if object.selected[0] >= object.size:
                object.selected[0] = 0
        else:
            pause = object.move([1,0])
    elif(key == "\n" and not pause and object.selecting):
        object.selecting = False
    elif(key == "r"):
        object = Board(boardSize)
        pause = False
        newHigh = False
    elif(key in ["s", "m", "l"]):
        boardSize = 10 if key=="s" else (15 if key=="m" else 18)
        object = Board(boardSize)
        pause = False
        newHigh = False
        rows, cols = stdscr.getmaxyx()
        x = boardSize*2 + 5
        info = curses.newwin(25, cols-x-5, 0, x)

    object.isGameOver = pause

    object.__str__(stdscr)
    if object.score > int(hScore):
        updateHScore(object.score)
        hScore = readHScore()
        newHigh = True

    stdscr.addstr("\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    if(not pause):
        info.addstr("Instructions:\n\n")
        if(object.selecting):
            info.addstr("Use the ArrowKeys to select a number\n\n")
            info.addstr("Press return to choose a starting position\n")
        else:
            info.addstr("Use the ArrowKeys to move\n")
            info.addstr("\nThe first adjacent number in that direction is how many positions will be moved\n\n")
    else:
        info.addstr("Game Over\n\n", curses.A_BLINK)
        if(newHigh):
            info.addstr("New High Score!\n\n", curses.A_BLINK)
        else:
            info.addstr("You didnt beat the high score\n\n")
    info.addstr("Use the 'S', 'M' or 'L' keys to resize\n")
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()

    if(key != "q"):
        key = "-1"
    return key, object, pause, hScore, boardSize, newHigh, info

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_GREEN)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    boardSize = 10
    object = Board(boardSize)
    object.__str__(stdscr)
    rows, cols = stdscr.getmaxyx()
    x = boardSize*2 + 5
    info = curses.newwin(25, cols-x-5, 0, x)
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')

    pause = False
    newHigh = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "\n", "q", "r", "s", "m", "l"]
    info.clear()
    info.addstr("Instructions:\n\n")
    info.addstr("Use the ArrowKeys to select a number\n\n")
    info.addstr("Press return to choose a starting position\n")
    info.addstr("Use the 'S', 'M' or 'L' keys to resize\n")
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()
    key = stdscr.getkey()
    while str(key) != "q":
        key, object, pause, hScore, boardSize, newHigh, info = gameLoop(stdscr, info, key, keys, object, pause, hScore, boardSize, newHigh)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
