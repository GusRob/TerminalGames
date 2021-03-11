import math
import time
import random
import curses
import os.path
from curses import wrapper

    ######    #       #     #   #
   #    # #  #         #   #   #
   #   #  #   #####     # #     #####
   #  #   #  #           #     #
   # #    #   #####     # #     #####
   ##     #        #   #   #         #
    ######    #####   #     #   #####

   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line board game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self, isX):
        self.state = [[" " for i in range(3)] for j in range(3)]
        self.isWinnerX = False
        self.isWinnerO= False
        self.score = 0
        self.isUserX = isX
        self.selected = [1,1]
    def makeTurn(self):
        empties = self.getEmpty()
        chosen = empties[random.randint(0, len(empties)-1)]
        self.state[chosen[0]][chosen[1]]  = ("O" if self.isUserX else "X")
        self.checkWinning()
        return
    def getEmpty(self):
        result = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == " ":
                    result.append([i,j])
        return result
    def checkWinning(self):
        trans = list(zip(*self.state)) #transposed matrix
        threes = []
        for i in range(3):
            threes.append("".join(self.state[i]))
            threes.append("".join(trans[i]))
        threes.append(self.state[0][0] + self.state[1][1] + self.state[2][2])
        threes.append(self.state[2][0] + self.state[1][1] + self.state[0][2])
        if "XXX" in threes:
            self.isWinnerX = True
        if "OOO" in threes:
            self.isWinnerO = True
        if self.getEmpty == []:
            self.isWinnerX = True
            self.isWinnerO = True
        return
    def __str__(self):
        result = ["╔═══╦═══╦═══╗\n", "", "", True]
        part = 0
        for i in range(3):
            for j in range(3):
                if self.selected[0] == j and self.selected[1] == i:
                    if(self.state[j][i] == " "):
                        result[3] = False
                    result[part] += "║ "
                    part += 1
                    result[part] += self.state[j][i] + " "
                    part += 1
                else:
                    result[part] += "║ " + self.state[j][i] + " "
            result[part] += "║\n"
            if i != 2:
                result[part] +="╠═══╬═══╬═══╣\n"
        result[part] += "╚═══╩═══╩═══╝"

        return result

def isAnInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

stdscr = curses.initscr() #initialise curses
curses.noecho()             #turn off echoing of keys to screen
curses.cbreak()              #allow game to react to key presses without waiting for return key
stdscr.keypad(True)         #cause special keys to be returned in curses format

def readHScore():
    result = [-1]
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        result = lines[3][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[3][1] = score
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

def gameLoop(stdscr, info, key, keys, object, pause, won, hScore):
    while not str(key) in keys:
        key = stdscr.getkey()
    stdscr.clear()

    if(key == "KEY_UP" and not pause):
        object.selected[1] = object.selected[1]-1
        if object.selected[1] <= -1:
            object.selected[1] = 2
    elif(key == "KEY_DOWN" and not pause):
        object.selected[1] = object.selected[1]+1
        if object.selected[1] >= 3:
            object.selected[1] = 0
    elif(key == "KEY_LEFT" and not pause):
        object.selected[0] = object.selected[0]-1
        if object.selected[0] <= -1:
            object.selected[0] = 2
    elif(key == "KEY_RIGHT" and not pause):
        object.selected[0] = object.selected[0]+1
        if object.selected[0] >= 3:
            object.selected[0] = 0
    elif(key == "\n" and not pause):
        object.state[object.selected[0]][object.selected[1]]  = ("X" if object.isUserX else "O")
        object.checkWinning()
        if (not object.isWinnerO) and (not object.isWinnerX):
            object.makeTurn()
        if object.isWinnerO or object.isWinnerX:
            pause = True
            if not (object.isWinnerO and object.isWinnerX):
                if object.isWinnerO and not object.isUserX:
                    won = True
                elif object.isWinnerX and object.isUserX:
                    won = True
    elif(key == "o" and object.isUserX):
        object = Board(False)
        object.makeTurn()
        pause = False
        won = False
    elif(key == "x" and not object.isUserX):
        object = Board(True)
        pause = False
        won = False
    elif(key == "r"):
        object = Board(object.isUserX)
        pause = False
        won = False

    output = object.__str__()
    stdscr.addstr(output[0], curses.color_pair(1))
    if output[3]:
        stdscr.addstr(output[1], curses.color_pair(2))
    else :
        stdscr.addstr(("X " if object.isUserX else "O "), curses.color_pair(3) | curses.A_BLINK)
    stdscr.addstr(output[2], curses.color_pair(1))
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    info.addstr("Instructions:\n")
    info.addstr("Use the ArrowKeys to select a box\n")
    info.addstr("Press return to place an " + ("X" if object.isUserX else "O"))
    info.addstr("\nMake three in a row to win!\n\n")
    info.addstr("Can you beat the computer?\n\n")
    info.addstr("Use the '" + ("O" if object.isUserX else "X") + "' key to change token\n")
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()

    if(key != "q"):
        key = "-1"
    return key, object, pause, won, hScore

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    object = Board(True)
    output = object.__str__()
    rows, cols = stdscr.getmaxyx()
    x = len(output[0].split('\n')[0])
    info = curses.newwin(25, cols-x, 0, x+2)
    stdscr.addstr(output[0], curses.color_pair(1))
    if output[3]:
        stdscr.addstr(output[1], curses.color_pair(2))
    else :
        stdscr.addstr(("X " if object.isUserX else "O "), curses.color_pair(3) | curses.A_BLINK)
    stdscr.addstr(output[2], curses.color_pair(1))
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')

    pause = False
    won = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "\n", "q", "r", "o", "x"]
    info.clear()
    info.addstr("Instructions:\n")
    info.addstr("Use the ArrowKeys to select a box\n")
    info.addstr("Press return to place an " + ("X" if object.isUserX else "O"))
    info.addstr("\nMake three in a row to win!\n\n")
    info.addstr("Can you beat the computer?\n\n")
    info.addstr("Use the '" + ("O" if object.isUserX else "X") + "' key to change token\n")
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()
    key = stdscr.getkey()
    while str(key) != "q":
        key, object, pause, won, hScore = gameLoop(stdscr, info, key, keys, object, pause, won, hScore)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
