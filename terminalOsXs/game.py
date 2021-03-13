import math
import time
import random
import curses
import os.path
from curses import wrapper
from collections import Counter

#  ██████╗ ██╗  ██╗ ██████╗ ██╗  ██╗
# ██╔═══██╗╚██╗██╔╝██╔═══██╗╚██╗██╔╝
# ██║   ██║ ╚███╔╝ ██║   ██║ ╚███╔╝
# ██║   ██║ ██╔██╗ ██║   ██║ ██╔██╗
# ╚██████╔╝██╔╝ ██╗╚██████╔╝██╔╝ ██╗
#  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝

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
    def resetBoard(self):
        self.state = [[" " for i in range(3)] for j in range(3)]
        self.selected = [1,1]
        self.isWinnerX = False
        self.isWinnerO= False
        self.isUserX = not self.isUserX
        if not self.isUserX:
            self.makeTurn()
    def makeTurn(self):
        bestMove = self.bestTurn()
        self.state[bestMove[0]][bestMove[1]]  = ("O" if self.isUserX else "X")
        self.checkWinning()
        return
    def valueFinal(self, isWinnerXTmp, isWinnerOTmp, isForX): #returns 1 if player isforx won ## returns -100 if game in progress
        result = -2                                         #returns -1 if player isforx lost ## returns 0 if game is a tie
        if (isForX and isWinnerXTmp and (not isWinnerOTmp)) or ((not isForX) and isWinnerOTmp and (not isWinnerXTmp)):
            result = 1
        if (isForX and isWinnerOTmp and (not isWinnerXTmp)) or ((not isForX) and isWinnerXTmp and (not isWinnerOTmp)):
            result = -1
        if (isWinnerOTmp and isWinnerXTmp):
            result = 0
        return result
    def bestTurn(self):
        moves = self.getEmpty(self.state)
        move = moves[random.randint(0,len(moves)-1)]
        bestFound = False
        if len(moves) == 9:
            corners = [[0,0],[2,2],[0,2],[2,0]]
            move = corners[random.randint(0,3)]
        else:
            stateTmp = [row[:] for row in self.state]
            for m in moves: #make winning moves
                stateTmp[m[0]][m[1]]  = ("O" if self.isUserX else "X")
                wOTmp, wXTmp = self.checkWinningTmp(stateTmp)
                mVal = self.valueFinal(wXTmp, wOTmp, not self.isUserX)
                if(mVal == 1 or mVal == 0):
                    move = m
                    bestFound = True
                stateTmp[m[0]][m[1]]  = " "
            if(not bestFound):
                for m in moves:#block losing moves
                    stateTmp[m[0]][m[1]]  = ("X" if self.isUserX else "O")
                    wOTmp, wXTmp = self.checkWinningTmp(stateTmp)
                    mVal = self.valueFinal(wXTmp, wOTmp, not self.isUserX)
                    if(mVal == -1):
                        move = m
                        bestFound = True
                    stateTmp[m[0]][m[1]]  = " "
        return move
    def getEmpty(self, stateTmp):
        result = []
        for i in range(3):
            for j in range(3):
                if stateTmp[i][j] == " ":
                    result.append([i,j])
        return result
    def countTwoRow(self, stateTmp):
        trans = list(zip(*stateTmp)) #transposed matrix
        threes = []
        for i in range(3):
            threes.append("".join(stateTmp[i]))
            threes.append("".join(trans[i]))
        threes.append(stateTmp[0][0] + stateTmp[1][1] + stateTmp[2][2])
        threes.append(stateTmp[2][0] + stateTmp[1][1] + stateTmp[0][2])
        collect = Counter(threes)
        noOfXPairs = collect["XX "] + collect["X X"] + collect[" XX"]
        noOfOPairs = collect["OO "] + collect["O O"] + collect[" OO"]
        return noOfXPairs, noOfOPairs
    def checkWinningTmp(self, stateTmp):
        trans = list(zip(*stateTmp)) #transposed matrix
        threes = []
        for i in range(3):
            threes.append("".join(stateTmp[i]))
            threes.append("".join(trans[i]))
        threes.append(stateTmp[0][0] + stateTmp[1][1] + stateTmp[2][2])
        threes.append(stateTmp[2][0] + stateTmp[1][1] + stateTmp[0][2])
        isWinnerXTmp = False
        isWinnerOTmp = False
        if "XXX" in threes:
            isWinnerXTmp = True
        if "OOO" in threes:
            isWinnerOTmp = True
        if len(self.getEmpty(stateTmp))== 0:
            isWinnerXTmp = True
            isWinnerOTmp = True
        return isWinnerOTmp, isWinnerXTmp
    def checkWinning(self):
        self.isWinnerO, self.isWinnerX = self.checkWinningTmp(self.state)
        if self.isWinnerO and self.isWinnerX:
            self.score += 1
        elif self.isWinnerO and (not self.isUserX):
            self.score += 3
        elif self.isWinnerX and self.isUserX:
            self.score += 3
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

random.seed()
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

def gameLoop(stdscr, info, key, keys, object, pause, hScore):
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
        if(object.state[object.selected[0]][object.selected[1]] == " "):
            object.state[object.selected[0]][object.selected[1]]  = ("X" if object.isUserX else "O")
            object.checkWinning()
            if object.isWinnerO or object.isWinnerX:
                pause = True
            else :
                object.makeTurn()
            if object.isWinnerO or object.isWinnerX:
                pause = True
    elif(key == "o" and object.isUserX):
        object = Board(False)
        object.makeTurn()
        pause = False
    elif(key == "x" and not object.isUserX):
        object = Board(True)
        pause = False
    elif(key == "r"):
        object = Board(object.isUserX)
        pause = False
        if not object.isUserX:
            object.makeTurn()
    elif(key == "c"):
        object.resetBoard()
        pause = False

    output = object.__str__()
    stdscr.addstr(output[0], curses.color_pair(1))
    if output[3]:
        stdscr.addstr(output[1], curses.color_pair(2))
    else :
        stdscr.addstr(("X " if object.isUserX else "O "), curses.color_pair(3) | curses.A_BLINK)
    stdscr.addstr(output[2], curses.color_pair(1))

    if object.score > int(hScore):
        updateHScore(object.score)
        hScore = readHScore()

    stdscr.addstr("\nYou Are: " + ("X" if object.isUserX else "O"))
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    if (not object.isWinnerO) and (not object.isWinnerX):
        info.addstr("Instructions:\n")
        info.addstr("Use the ArrowKeys to select a box\n")
        info.addstr("Press return to place an " + ("X" if object.isUserX else "O"))
        info.addstr("\nMake three in a row to win!\n\n")
        info.addstr("Can you beat the computer?\n\n")
        info.addstr("Use the '" + ("O" if object.isUserX else "X") + "' key to change token\n")
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n")
    else :
        if object.isWinnerO and object.isWinnerX:
            info.addstr("Its a Tie!\n\n", curses.A_BLINK)
            info.addstr("Your Score has been increased by 1\n")
        else :
            if object.isWinnerO and (not object.isWinnerX):
                info.addstr("O Wins!\n\n", curses.A_BLINK)
            elif (not object.isWinnerO) and object.isWinnerX:
                info.addstr("X Wins!\n\n", curses.A_BLINK)
            if object.isWinnerO and (not object.isUserX):
                info.addstr("Your Score has been increased by 3\n")
            elif object.isWinnerX and object.isUserX:
                info.addstr("Your Score has been increased by 3\n")
            else:
                info.addstr("Your Score has not been increased\n")
        info.addstr("Use the 'C' key to begin the next game\n")
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()

    if(key != "q"):
        key = "-1"
    return key, object, pause, hScore

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
    info = curses.newwin(25, cols-x, 0, x+5)
    stdscr.addstr(output[0], curses.color_pair(1))
    if output[3]:
        stdscr.addstr(output[1], curses.color_pair(2))
    else :
        stdscr.addstr(("X " if object.isUserX else "O "), curses.color_pair(3) | curses.A_BLINK)
    stdscr.addstr(output[2], curses.color_pair(1))
    stdscr.addstr("\nYou Are: " + ("X" if object.isUserX else "O"))
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')

    pause = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "\n", "q", "r", "o", "x", "c"]
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
        key, object, pause, hScore = gameLoop(stdscr, info, key, keys, object, pause, hScore)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
