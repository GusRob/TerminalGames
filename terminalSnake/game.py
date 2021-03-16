import math
import time
import random
import time
import pygame
import curses
import os.path
from curses import wrapper
from collections import Counter

# ███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗
# ██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝
# ███████╗██╔██╗ ██║███████║█████╔╝ █████╗
# ╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝
# ███████║██║ ╚████║██║  ██║██║  ██╗███████╗
# ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#
   # A simple command line board game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self):
        self.hPos = [6,6]
        self.bPos = [self.hPos[:], self.hPos[:], self.hPos[:]]
        empties = self.getEmpty()
        self.fPos = empties[random.randint(0, len(empties))]
        self.score = 0
        self.gameOver = False
        self.dir = 0
        self.moveCounter = 0
        self.speed = 8
        self.dirChanged = False
        self.death = 225
        self.newHigh = False
        self.solidWalls = True
    def move(self):
        newHPos = self.hPos[:]
        if(self.dir == 0):
            newHPos[1] += 1
        elif(self.dir == 1):
            newHPos[0] += 1
        elif(self.dir == 2):
            newHPos[1] -= 1
        elif(self.dir == 3):
            newHPos[0] -= 1

        if max(newHPos) >= 15 or min(newHPos) <= -1:
            if(self.solidWalls):
                self.gameOver = True
                self.death = len(self.bPos)
            else:
                if(newHPos[0] >= 15):
                    newHPos[0] = 0
                elif(newHPos[1] >= 15):
                    newHPos[1] = 0
                elif(newHPos[0] <= -1):
                    newHPos[0] = 14
                elif(newHPos[1] <= -1):
                    newHPos[1] = 14

        if(newHPos in self.bPos[1:]):
            self.gameOver = True
            self.death = len(self.bPos)
        elif not self.gameOver:
            self.bPos.append(newHPos[:])
            self.hPos = newHPos
            if self.hPos == self.fPos :
                empties = self.getEmpty()
                self.fPos = empties[random.randint(0, len(empties))]
                self.speed = 10-int(len(self.bPos)/2)
                if(self.speed < 2):
                    self.speed = 2
                self.score += 1
            else :
                self.bPos.pop(0)
            self.dirChanged = False
    def getEmpty(self):
        result = []
        for i in range(15):
            for j in range(15):
                if not [i,j] in self.bPos:
                    result.append([i,j])
        return result
    def __str__(self, stdscr):
        stdscr.addstr("╔═══════════════════════════════╗\n")
        part = 0
        for i in range(15):
            stdscr.addstr("║ ")
            for j in range(15):
                if [i,j] == self.hPos:
                    heads = ["▶ ", "▼ ", "◀ ", "▲ "]
                    if(self.gameOver):
                        stdscr.addstr(heads[self.dir], curses.color_pair(2))
                    else:
                        stdscr.addstr(heads[self.dir], curses.color_pair(3))
                elif [i,j] in self.bPos:
                    if self.death < self.bPos.index([i,j]):
                        stdscr.addstr("● ", curses.color_pair(2))
                    else:
                        stdscr.addstr("● ", curses.color_pair(3))
                elif [i,j] == self.fPos:
                    stdscr.addstr(" ", curses.color_pair(2))
                else:
                   stdscr.addstr("  ", curses.color_pair(3))

            stdscr.addstr("║\n")
        stdscr.addstr("╚═══════════════════════════════╝\n")

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
stdscr.nodelay(True)         #game doesnt wait for user to press a key
clock = pygame.time.Clock()

def readHScore():
    result = [-1]
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        result = lines[5][1]
    return result

def updateHScore(score):
    with open(os.path.join(os.path.dirname(__file__), 'HiScores.txt'), "r") as textFile:
        lines = [line.split() for line in textFile]
        lines[5][1] = score
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

    if(key == curses.KEY_UP and (not pause) and (not object.dirChanged)):
        if object.dir != 1:
            object.dir = 3
            object.dirChanged = True
    elif(key == curses.KEY_DOWN and (not pause) and (not object.dirChanged)):
        if object.dir != 3:
            object.dir = 1
            object.dirChanged = True
    elif(key == curses.KEY_LEFT and (not pause) and (not object.dirChanged)):
        if object.dir != 0:
            object.dir = 2
            object.dirChanged = True
    elif(key == curses.KEY_RIGHT and (not pause) and (not object.dirChanged)):
        if object.dir != 2:
            object.dir = 0
            object.dirChanged = True
    elif(key == ord('r')):
        newWalls = object.solidWalls
        object = Board()
        object.solidWalls = newWalls
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
            object.move()

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
        info.addstr("Use the ArrowKeys to move\n")
        info.addstr("Eat the food to Grow!\n")
        info.addstr("Can you grow the largest?\n\n")
        info.addstr("Walls are currently \n" + ("infinite\n" if not object.solidWalls else "solid\n"))
        info.addstr("\nUse the 'I' key to \n" + ("make walls infinite\n" if object.solidWalls else "make walls solid\n"))
        info.addstr("Use the 'R' key to reset\n")
        info.addstr("Use the 'Q' key to quit\n\n")
    stdscr.refresh()
    info.refresh()


    time.sleep(0.05)

    return object, pause, hScore, key

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    object = Board()
    rows, cols = stdscr.getmaxyx()
    x = 40
    info = curses.newwin(rows, 35, 0, x)
    object.__str__(stdscr)

    if object.score > int(hScore):
        updateHScore(object.score)
        hScore = readHScore()

    pause = True
    keys = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_ENTER, ord('q'), ord('r'), ord('i')]

    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    info.clear()
    info.addstr("Instructions:\n")
    info.addstr("Use the ArrowKeys to move\n")
    info.addstr("Eat the food to Grow!\n")
    info.addstr("Can you grow the largest?\n\n")
    info.addstr("Walls are currently \n" + ("infinite\n" if not object.solidWalls else "solid\n"))
    info.addstr("\nUse the 'I' key to \n" + ("make walls infinite\n" if object.solidWalls else "make walls solid\n"))
    info.addstr("Use the 'R' key to reset\n")
    info.addstr("Use the 'Q' key to quit\n")
    stdscr.refresh()
    info.refresh()
    key = -1

    while key != ord('q'):
        object, pause, hScore, key = gameLoop(stdscr, info, key, keys, object, pause, hScore)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
