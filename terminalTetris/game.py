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
   # A simple command line board game in Python. #
   #*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*#

########################################################
########################################################

class Board:
    def __init__(self):
        self.state = [[" " for i in range(6)] for j in range(12)]
        self.gameOver = False
        self.moveCounter = 0
        self.speed = 0
        self.score = 0
        self.newHigh = False
    def move(self):
        return
    def deleteRow(self):
        return
    def __str__(self, stdscr):
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

        '''    if(key == curses.KEY_UP and (not pause)):
    elif(key == curses.KEY_DOWN and (not pause)):
    elif(key == curses.KEY_LEFT and (not pause)):
    elif(key == curses.KEY_RIGHT and (not pause)):
    elif(key == ord('r')):
        object = Board()
        pause = True
    elif(key == ord('i')):
        newWalls = not object.solidWalls
        object = Board()
        object.solidWalls = newWalls
        pause = True
        '''
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
