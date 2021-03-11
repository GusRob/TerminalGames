import math
import time
import random
import curses
import os.path
from curses import wrapper

   #######   ######   #      #    ######
         #  #    # #  #      #   #      #
         #  #   #  #  #      #   #      #
    #####   #  #   #   ######     ######
   #        # #    #         #   #      #
   #        ##     #         #   #      #
   #######   ######          #    ######

   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line block game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self, size):
        self.size = size
        self.state = [["-1" for i in range(self.size)] for j in range(self.size)]
        self.newest = [-1,-1]
        self.isGameOver = False
        self.score = 0
        self.addNum()
        self.addNum()
    def getWidth(self):
        return max(len(str(val)) for line in self.state for val in line) + 2 * len(str(2**(self.size+1))) * self.size
    def moveRow(self, input):
        output = []
        scoreInc = 0
        for i in range(self.size) :         # remove blank spaces
            if input[i] != "-1" :
                output.append(str(input[i]))
        result = []
        i = 0
        while i < len(output) :
            if(i != len(output)-1):         #if two in a row, collapse into 1
                if output[i] == output[i+1] and output[i] != "-1":
                    result.append(str(int(output[i])+1))
                    scoreInc += 2**(int(output[i])+1)
                    i+=1
                else :
                    result.append(str(output[i]))
            else :
                result.append(str(output[i]))
            i += 1
        i = len(result)
        while i < self.size :         # fill blank spaces
            result.append("-1")
            i+=1
        return result, scoreInc
    def move(self, isVertical, isPositive):
        scoreInc = 0
        original = [row[:] for row in self.state]
        for i in range(self.size) : #for each column/row#
            rowToCollapse = []
            max = self.size if isPositive else -1
            j = 0 if isPositive else self.size-1
            while ((j < max) if isPositive else (j > max)):
                rowToCollapse.append(self.state[j][i] if isVertical else self.state[i][j])
                j += (1 if isPositive else -1)
            rowCollapsed, scoreIncInc = self.moveRow(rowToCollapse)
            scoreInc += scoreIncInc
            j = 0 if isPositive else self.size-1
            while ((j < max) if isPositive else (j > max)) :
                if isVertical :
                    self.state[j][i] = rowCollapsed[j if isPositive else self.size-j-1]
                else :
                    self.state[i][j] = rowCollapsed[j if isPositive else self.size-j-1]
                j += (1 if isPositive else -1)
        moveFailed = (original == self.state)
        return moveFailed, scoreInc
    def addNum(self):
        x, y = self.getRandEmpty()
        if x == -1 or y == -1 :
            self.isGameOver = True
        else :
            self.state[x][y] = str(1 + random.randint(0,1))
            self.newest = [x, y]
        return
    def getHighestVal(self):
        result = -1
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] != '-1':
                    val = int(self.state[i][j])
                    if val >= result:
                        result = val
        return 2**result
    def getRandEmpty(self):
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == "-1":
                    empty.append((i,j))
        gameOver = False
        if len(empty) == 0 :
            gameOver = True
        return (-1,-1) if gameOver else empty[random.randint(0, len(empty)-1)];
    def findNth(self, haystack, needle, n):
        needle = " " + needle + " "
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start
    def splitStr(self, toSplit, index, colWidth):
        result = [toSplit, "", ""]
        vals = toSplit.split()
        occurs = 1
        while "║" in vals:
            vals.remove("║")
        for i in range(len(vals)):
            if index != -1:
                if i < index and vals[i] == vals[index]:
                    occurs += 1
        result[0] = toSplit[:self.findNth(toSplit, vals[index], occurs) + 1]
        result[1] = vals[index]
        result[2] = toSplit[self.findNth(toSplit, vals[index], occurs)+len(str(vals[index]))+1:]

        result[0] = result[0].replace("0.5", "   ")
        result[2] = result[2].replace("0.5", "   ")
        return result
    def __str__(self):
        colWidth = 6  # padding
        part = 0
        result = ["╔", "", ""]
        for n in range(self.size):
            for j in range(colWidth):
                result[part] += "═"
            if n != self.size-1 :
                result[part] += "╦"
        result[part] += "╗\n"
        for i in range(self.size) :
            if i == self.newest[0]:
                line = [str(2**int(val)).center(colWidth) for val in self.state[i]]
                addition = "║".join(line)
                split = self.splitStr(addition, self.newest[1], colWidth)
                result[part] += "║" + split[0]
                part += 1
                result[part] += split[1]
                part +=1
                result[part] += split[2] + '║\n'
            else :
                line = [str(2**int(val) if val != '-1' else '').center(colWidth) for val in self.state[i]]
                addition = "║".join(line)
                result[part] += "║" + addition + '║\n'
            if i != self.size-1 :
                result[part] += "╠"
                for n in range(self.size):
                    for j in range(colWidth):
                        result[part] += "═"
                    if n != self.size-1 :
                        result[part] += "╬"
                result[part] += "╣\n"
        result[part] += "╚"
        for n in range(self.size):
            for j in range(colWidth):
                result[part] += "═"
            if n != self.size-1 :
                result[part] += "╩"
        result[part] += "╝\n"
        return result

def gameLoop(key, keys, won, pause, stdscr, info, boardSize, object, hScore):
    while not str(key) in keys:
        key = stdscr.getkey()
    stdscr.clear()
    moveFailed = False
    scoreInc = 0
    original = [row[:] for row in object.state]
    if(key == "KEY_UP" and not pause):
        moveFailed, scoreInc = object.move(True, True)
    elif(key == "KEY_DOWN" and not pause):
        moveFailed, scoreInc = object.move(True, False)
    elif(key == "KEY_LEFT" and not pause):
        moveFailed, scoreInc = object.move(False, True)
    elif(key == "KEY_RIGHT" and not pause):
        moveFailed, scoreInc = object.move(False, False)
    elif(key == "r"):
        object = Board(boardSize)
        pause = False
        won = False
    elif(key == "c" and pause and not object.isGameOver):
        pause = False
        won = True
    elif(isAnInt(key)):
        boardSize = int(key)
        object = Board(boardSize)
        output = object.__str__()
        rows, cols = stdscr.getmaxyx()
        x = len(output[0].split('\n')[0])
        info = curses.newwin(25, cols-x, 0, x)
    if(moveFailed):
        test1, _ = object.move(False, False)
        object.state = [row[:] for row in original]
        test2, _ = object.move(False, True)
        object.state = [row[:] for row in original]
        test3, _ = object.move(True, False)
        object.state = [row[:] for row in original]
        test4, _ = object.move(True, True)
        object.state = [row[:] for row in original]

        if(test1 and test2 and test3 and test4):
            object.isGameOver = True
    else:
        object.score += scoreInc
    if key != "r" and key != "c" and key != "q" and not isAnInt(key) and not pause and not moveFailed:
        object.addNum()
    info.clear()
    output = object.__str__()
    stdscr.addstr(output[0], curses.color_pair(1))
    stdscr.addstr(output[1], curses.color_pair(2))
    stdscr.addstr(output[2], curses.color_pair(1))
    if(object.isGameOver):
        pause = True
        stdscr.addstr("GAME OVER\n", curses.A_BLINK)
        stdscr.addstr("You Scored: " + str(object.score) + '\n')
        if(int(hScore)>int(object.score)):
            stdscr.addstr("High Score: " + str(hScore) +'\n')
        else :
            stdscr.addstr("High Score: " + str(object.score) +'\n')
            hScore = updateHScore(object.score)
        stdscr.addstr("\nPress 'R' to Restart")
    else :
        stdscr.addstr("Your Score: " + str(object.score) + '\n')
        if(int(hScore)>int(object.score)):
            stdscr.addstr("High Score: " + str(hScore) +'\n')
        else :
            stdscr.addstr("High Score: " + str(object.score) +'\n')

    if(object.getHighestVal() >= 2048 and not won):
        pause = True
        info.addstr("YOU WIN\n", curses.A_BLINK)
        info.addstr("Press 'C' to Continue\n")
        info.addstr("Or 'R' to Restart")
    else :
        info.addstr("Instructions:\n")
        info.addstr("Use the ArrowKeys to slide the blocks\n")
        info.addstr("When blocks slide into each other,\nthey combine to double the value!\n\n")
        info.addstr("Try to reach 2048\n")
        info.addstr("How far can you get?\n\n")
        info.addstr("Use the num keys 2-6 to change the size of the game\n")
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()
    if(key != "q"):
        key = "-1"
    return key, object, info, pause, won, boardSize, hScore

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
        result = lines[1][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[1][1] = score
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


def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    boardSize = 4
    object = Board(boardSize)
    output = object.__str__()
    rows, cols = stdscr.getmaxyx()
    x = len(output[0].split('\n')[0])
    info = curses.newwin(25, cols-x, 0, x)
    stdscr.addstr(output[0], curses.color_pair(1))
    stdscr.addstr(output[1], curses.color_pair(2))
    stdscr.addstr(output[2], curses.color_pair(1))
    stdscr.addstr("Your Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')

    pause = False
    won = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "q", "r", "c", "2", "3", "4", "5", "6"]
    info.clear()
    info.addstr("Instructions:\n")
    info.addstr("Use the ArrowKeys to slide the blocks\n")
    info.addstr("When blocks slide into each other,\nthey combine to double the value!\n\n")
    info.addstr("Try to reach 2048\n")
    info.addstr("How far can you get?\n\n")
    info.addstr("Use the num keys 2-6 to change the size of the game\n")
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()
    key = stdscr.getkey()
    while str(key) != "q":
        key, object, info, pause, won, boardSize, hScore = gameLoop(key, keys, won, pause, stdscr, info, boardSize, object, hScore)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
