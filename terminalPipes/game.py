import math
import time
import random
import curses
import os.path
from curses import wrapper
from collections import Counter

#  ██████╗ ██╗██████╗ ███████╗███████╗
#  ██╔══██╗██║██╔══██╗██╔════╝██╔════╝
#  ██████╔╝██║██████╔╝█████╗  ███████╗
#  ██╔═══╝ ██║██╔═══╝ ██╔══╝  ╚════██║
#  ██║     ██║██║     ███████╗███████║
#  ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝


   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line maze puzzle game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################


# NEEDS REVISITING - METHODS NEED TO BE MORE CONCISE, COMMENTING

#   ═   ║   ╔   ╦   ╗   ╠   ╬   ╣   ╚   ╩   ╝
class Board:
    def __init__(self):
        self.state = [[11 for i in range(40)] for j in range(20)]
        self.score = 0
        self.selected = [1,1]
        self.held = 0
        self.gameOver = False
        self.pathComplete = False
        self.openEnds = 0
        self.start = 0#random.randint(0, 40)
        self.finish = 0#random.randint(0, 40)
        self.queue = self.generateQueue()
    def generateQueue(self):
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        #return [0,1,2,3,4,5,6,7,8,9,10,11]
    def checkPath(self,current,last, stdscr):
        result = True
        stdscr.addstr("testing " + str(current) + ": ")
        if current[0] > -1 and current[0] < len(self.state):
            if self.state[current[0]][current[1]] == 11:
                #stdscr.addstr("check1 ")
                result = False
            else:
                if (not [current[0], current[1]+1] == last) and self.state[current[0]][current[1]] in [0,2,4,6,7,9,10]: # exits right
                    result = result and self.checkPath([current[0], current[1]+1], current, stdscr)
                if (not [current[0], current[1]-1] == last) and self.state[current[0]][current[1]-1] in [0,3,5,7,8,9,10]: # exits left
                    result = result and self.checkPath([current[0], current[1]+1], current, stdscr)
                if (not [current[0]+1, current[1]] == last) and self.state[current[0]][current[1]] in [1,2,3,6,7,8,9]: # exits down
                    result = result and self.checkPath([current[0]+1, current[1]], current, stdscr)
                if (not [current[0]-1, current[1]] == last) and self.state[current[0]][current[1]] in [1,4,5,6,8,9,10]: # exits up
                    result = result and self.checkPath([current[0]-1, current[1]], current, stdscr)
        else :
            result = False
        #stdscr.addstr(str(result) + "\n")
        return result
    def update(self, stdscr):
        if not self.pathComplete:
            self.pathComplete = self.checkPath([self.start,0],[self.start,-1], stdscr)
        if (not self.pathComplete) and (self.held == 11):
            self.gameOver = True
        if self.pathComplete and self.openEnds <= 1:
            self.gameOver = True
        return
    def __str__(self, stdscr):
        stdscr.addstr("╔═", curses.color_pair(3))
        for i in range(len(self.state[0])):
            if(i == self.start):
                stdscr.addstr("╦", curses.color_pair(3))
            else:
                stdscr.addstr("═", curses.color_pair(3))
        stdscr.addstr("═╗", curses.color_pair(3))
        stdscr.addstr("Current:\n")
        nextTop = "╔═══╗"
        nextBot = "╚═══╝"
        opts = ["═","║","╔","╗","╚","╝","╠","╦","╣","╬","╩", " "]
        for i in range(len(self.state)):
            borderCol = 3 if i < 10 else (2 if i == 10 else (3 if self.pathComplete else 1))
            stdscr.addstr("║ " if i != 10 else "X ", curses.color_pair(borderCol))
            for j in range(len(self.state[0])):
                if( [i,j] == self.selected):
                    if(self.state[i][j] == 11):
                        stdscr.addstr(opts[self.held], curses.color_pair(4))
                    else:
                        stdscr.addstr(opts[self.state[i][j]], curses.color_pair(2))
                else:
                    stdscr.addstr(opts[self.state[i][j]])
            stdscr.addstr(" ║" if i != 10 else " X", curses.color_pair(borderCol))
            if(i == 0):
                stdscr.addstr(nextTop)
            elif(i == 1):
                stdscr.addstr("║ ")
                stdscr.addstr(opts[self.held], curses.color_pair(4))
                stdscr.addstr(" ║")
            elif(i == 2):
                stdscr.addstr(nextBot)
            elif(i == 3):
                stdscr.addstr("Next:")
            if(i > 3):
                if (i-1)%3 == 0 and i < 19:
                    stdscr.addstr(nextTop)
                elif (i)%3 == 0 and i < 19:
                    stdscr.addstr(nextBot)
                elif (i-2)%3 == 0 and i < 19:
                    index = int((i-1)/3)
                    stdscr.addstr("║ " + opts[self.queue[index]] + " ║")
            stdscr.addstr("\n")
        baseCol = curses.color_pair(3 if self.pathComplete else 1)
        stdscr.addstr("╚═", baseCol)
        for i in range(len(self.state[0])):
            if(i == self.finish):
                stdscr.addstr("╩", baseCol)
            else:
                stdscr.addstr("═", baseCol)
        stdscr.addstr("═╝\n", baseCol)
        return


random.seed()
stdscr = curses.initscr() #initialise curses
curses.noecho()             #turn off echoing of keys to screen
curses.cbreak()              #allow game to react to key presses with waiting for return key
stdscr.keypad(True)         #cause special keys to be returned in curses format

def readHScore():
    result = [-1]
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        result = lines[7][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[7][1] = score
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
        object.selected[0] -= 1
        if(object.selected[0] <= -1):
            object.selected[0] = len(object.state) - 1
    elif(key == "KEY_DOWN" and not pause):
        object.selected[0] += 1
        if(object.selected[0] >= len(object.state)):
            object.selected[0] = 0
    elif(key == "KEY_LEFT" and not pause):
        object.selected[1] -= 1
        if(object.selected[1] <= -1):
            object.selected[1] = len(object.state[0]) - 1
    elif(key == "KEY_RIGHT" and not pause):
        object.selected[1] += 1
        if(object.selected[1] >= len(object.state[0])):
            object.selected[1] = 0
    elif(key == "\n" and not pause):
        if(object.state[object.selected[0]][object.selected[1]] == 11):
            object.state[object.selected[0]][object.selected[1]] = object.held
            object.held = object.queue[0]
            object.queue.pop(0)
            while(len(object.queue) < 6):
                object.queue += [11]
            object.update(stdscr)
    elif(key == "r"):
        object = Board()
        pause = False


    object.__str__(stdscr)

    if object.score > int(hScore):
        updateHScore(object.score)
        hScore = readHScore()

    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    if (not object.gameOver):
        info.addstr("Instructions:\n")
        info.addstr("Use the ArrowKeys to move the pipe\n")
        info.addstr("Press return to place a pipe\n")
        info.addstr("Complete the circuit to win!\n\n")
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n")
    else :
        pause = True
        if object.pathComplete and object.openEnds == 0 :
            info.addstr("You Win!!\n")
            info.addstr("Nice Job\n")
        else:
            info.addstr("Game Over You Lose!\n\n")
            info.addstr("Remember the pipe needs to be complete!\n")
            info.addstr("No Loose ends!\n")
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
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    object = Board()
    object.__str__(stdscr)
    rows, cols = stdscr.getmaxyx()
    x = 50
    info = curses.newwin(25, cols-x, 0, x+5)
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')

    pause = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "\n", "q", "r"]
    info.clear()
    info.addstr("Instructions:\n")
    info.addstr("Use the ArrowKeys to move the pipe\n")
    info.addstr("Press return to place a pipe\n")
    info.addstr("Complete the circuit to win!\n\n")
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
