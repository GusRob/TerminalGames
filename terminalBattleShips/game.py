import math
import time
import random
import curses
import os.path
from curses import wrapper
from collections import Counter

# ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ ███████╗
# ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗██╔════╝
# ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝███████╗
# ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ ╚════██║
# ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     ███████║
# ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝

   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line board game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self, size):
        self.size = size
        self.state = [[["≈" for i in range(size)] for j in range(size)], [["≈" for i in range(size)] for j in range(size)]]
        self.score = 0
        self.mode = "placing"
        self.held = 5
        self.heldO = 0
        self.valid = False
        self.selected = [1,1]
        self.shipSigns = ["⌖ ", "▲ ", "▶ ", "▼ ", "◀ ", "■ ", "◌ ", "≈ "]
    def __str__(self, stdscr):
        falses = [False, False, False, False, False]
        drawVal(stdscr, "Your Targets: " + "Your Ships:".rjust(self.size * 2 + 1) + "\n╔", falses)
        for i in range(self.size * 2 + 1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╗\t╔", falses)
        for i in range(self.size * 2 + 1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╗\n", falses)
        for i in range(self.size):
            drawVal(stdscr, "║ ", falses)
            for j in range(self.size):
                if self.selected[0] == j and self.selected[1] == i and self.mode != "placing":
                    drawVal(stdscr, self.state[0][j][i] + " ", [True, False, False, False, False])
                else:
                    drawVal(stdscr, self.state[0][j][i] + " ", falses)
            drawVal(stdscr, "║\t║ ", falses)
            for j in range(self.size):
                if(self.mode == "placing"):
                    ship = []
                    xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
                    yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
                    for n in range(self.held):
                        ship.append([self.selected[0] + xDir*n, self.selected[1] + yDir*n])
                    if [j,i] in ship:
                        ends = ["▶ ", "▼ ", "◀ ", "▲ "]
                        starts = ["◀ ", "▲ ", "▶ ", "▼ "]
                        if(ship.index([j,i]) == 0):
                            drawVal(stdscr, starts[self.heldO], [True, False, False, True, self.valid])
                        elif(ship.index([j,i]) == len(ship)-1):
                            drawVal(stdscr, ends[self.heldO], [True, False, False, True, self.valid])
                        else:
                            drawVal(stdscr, "■ ", [True, False, False, True, self.valid])
                    else:
                        drawVal(stdscr, self.state[1][j][i] + " ", falses)
                else:
                    drawVal(stdscr, self.state[1][j][i] + " ", falses)
            drawVal(stdscr, "║\n", falses)
        drawVal(stdscr, "╚", falses)
        for i in range(self.size * 2 +1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╝\t╚", falses)
        for i in range(self.size * 2 +1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╝\n", falses)
        return
    def placeHeld(self):
        ship = []
        xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
        yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
        for n in range(self.held):
            ship.append([self.selected[0] + xDir*n, self.selected[1] + yDir*n])
        for i in range(len(ship)):
            part = ship[i]
            ends = ["▶", "▼", "◀", "▲"]
            starts = ["◀", "▲", "▶", "▼"]
            if(i == 0):
                self.state[1][part[0]][part[1]] = starts[self.heldO]
            elif(i == len(ship)-1):
                self.state[1][part[0]][part[1]] = ends[self.heldO]
            else:
                self.state[1][part[0]][part[1]] = "■"
        self.held = self.held-1 if (self.held != 2) else 2
        self.selected = [0,0]
    def updateValid(self):
        result = True
        ship = []
        xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
        yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
        for n in range(self.held):
            ship.append([self.selected[0] + xDir*n, self.selected[1] + yDir*n])
        for i in range(len(ship)):
            part = ship[i]
            if(part[0] <= -1 or part[0] >= self.size or part[1] <= -1 or part[1] >= self.size):
                result = False
            elif self.state[1][part[0]][part[1]] in ["▲", "▶", "▼", "◀", "■"]:
                result = False
        self.valid = result


def drawVal(stdscr, val, bools): # w r g b
    selected, hit, sunk, placing, valid = bools
    if placing:
        if valid:
            stdscr.addstr(val, curses.color_pair(3))
        else :
            stdscr.addstr(val, curses.color_pair(2))
    elif selected:
        if val in ["⌖ ", "▲ ", "▶ ", "▼ ", "◀ ", "■ "]:
            stdscr.addstr(val, curses.color_pair(2))
        else :
            stdscr.addstr(val, curses.color_pair(3))
    elif hit:
        stdscr.addstr(val, curses.color_pair(1))
    elif sunk:
        stdscr.addstr(val, curses.color_pair(2))
    elif val == "≈ ":
        stdscr.addstr(val, curses.color_pair(4))
    elif val == "◌ ":
        stdscr.addstr(val, curses.color_pair(4))
    else:
        stdscr.addstr(val, curses.color_pair(1))


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
        result = lines[4][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[4][1] = score
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

def gameLoop(stdscr, info, key, keys, object, pause, hScore, boardSize):
    while not str(key) in keys:
        key = stdscr.getkey()
    stdscr.clear()

    if(key == "KEY_UP" and not pause):
        object.selected[1] = object.selected[1]-1
        if object.selected[1] <= -1:
            object.selected[1] = boardSize-1
        object.updateValid()
    elif(key == "KEY_DOWN" and not pause):
        object.selected[1] = object.selected[1]+1
        if object.selected[1] >= boardSize:
            object.selected[1] = 0
        object.updateValid()
    elif(key == "KEY_LEFT" and not pause):
        object.selected[0] = object.selected[0]-1
        if object.selected[0] <= -1:
            object.selected[0] = boardSize-1
        object.updateValid()
    elif(key == "KEY_RIGHT" and not pause):
        object.selected[0] = object.selected[0]+1
        if object.selected[0] >= boardSize:
            object.selected[0] = 0
        object.updateValid()
    elif(key == " " and not pause):
        if object.mode == "placing":
            object.heldO += 1;
            if(object.heldO >= 4):
                object.heldO = 0
        object.updateValid()
    elif(key == "\n" and not pause):
        if object.mode == "placing" and object.valid:
            object.placeHeld()
        object.updateValid()
    elif(key == "r" or key=="s" or key=="m" or key=="l"):
        if key == "s":
            boardSize = 7
        elif key == "m":
            boardSize = 10
        elif key == "l":
            boardSize = 13
        object = Board(boardSize)
        pause = False
    object.__str__(stdscr)
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    stdscr.refresh()
    info.refresh()

    if(key != "q"):
        key = "-1"
    return key, object, pause, hScore, boardSize

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    boardSize = 10
    object = Board(boardSize)
    object.__str__(stdscr)
    rows, cols = stdscr.getmaxyx()
    x = 20
    info = curses.newwin(25, cols-x, 0, x+50)

    pause = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", " ", "\n", "q", "r", "s", "m", "l"]
    info.clear()
    stdscr.refresh()
    info.refresh()
    key = stdscr.getkey()
    while str(key) != "q":
        key, object, pause, hScore, boardSize = gameLoop(stdscr, info, key, keys, object, pause, hScore, boardSize)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
