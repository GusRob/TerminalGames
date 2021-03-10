import math
import time
import random
import curses
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
        self.state = [["" for i in range(self.size)] for j in range(self.size)]
        self.addNum()
        self.addNum()
    def getWidth(self):
        return max(len(str(val)) for line in self.state for val in line) + 2 * len(str(2**(self.size+1))) * self.size
    def moveRow(self, input):
        output = []
        for i in range(self.size) :         # remove blank spaces
            if input[i] != "" :
                output.append(input[i])
        result = []
        i = 0
        while i < len(output) :
            if(i != len(output)-1):         #if two in a row, collapse into 1
                if output[i] == output[i+1] :
                    result.append(str(int(output[i])+1))
                    i+=1
                else :
                    result.append(str(output[i]))
            else :
                result.append(str(output[i]))
            i += 1
        i = len(result)
        while i < self.size :         # fill blank spaces
            result.append("")
            i+=1
        return result
    def move(self, isVertical, isPositive):
        for i in range(self.size) : #for each column/row#
            rowToCollapse = []
            max = self.size if isPositive else -1
            j = 0 if isPositive else self.size-1
            while ((j < max) if isPositive else (j > max)):
                rowToCollapse.append(self.state[j][i] if isVertical else self.state[i][j])
                j += (1 if isPositive else -1)
            rowCollapsed = self.moveRow(rowToCollapse)
            j = 0 if isPositive else self.size-1
            while ((j < max) if isPositive else (j > max)) :
                if isVertical :
                    self.state[j][i] = rowCollapsed[j if isPositive else self.size-j-1]
                else :
                    self.state[i][j] = rowCollapsed[j if isPositive else self.size-j-1]
                j += (1 if isPositive else -1)
        return
    def addNum(self):
        x, y = self.getRandEmpty()
        self.state[x][y] = (1 + random.randint(0,1))
        return
    def getRandEmpty(self):
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == "":
                    empty.append((i,j))
        return empty[random.randint(0, len(empty)-1)];
    def __str__(self):
        colWidth = max(len(str(val)) for line in self.state for val in line) + 2 * len(str(2**(self.size+1)))  # padding
        result = "╔"
        for n in range(self.size):
            for j in range(colWidth):
                result += "═"
            if n != self.size-1 :
                result += "╦"
        result += "╗\n"
        for i in range(self.size) :
            line = [str(2**int(val) if val != '' else '').center(colWidth) for val in self.state[i]]
            addition = "║".join(line)
            result += "║" + addition + '║\n'
            if i != self.size-1 :
                result += "╠"
                for n in range(self.size):
                    for j in range(colWidth):
                        result += "═"
                    if n != self.size-1 :
                        result += "╬"
                result += "╣\n"
        result += "╚"
        for n in range(self.size):
            for j in range(colWidth):
                result += "═"
            if n != self.size-1 :
                result += "╩"
        result += "╝\n"
        return result


stdscr = curses.initscr() #initialise curses
curses.noecho()             #turn off echoing of keys to screen
curses.cbreak()              #allow game to react to key presses without waiting for return key
stdscr.keypad(True)         #cause special keys to be returned in curses format

def main(stdscr):           #main function is entry point to game
    # Clear screen
    stdscr.clear()
    object = Board(4)
    stdscr.addstr(object.__str__())
    stdscr.refresh()
    key = stdscr.getkey()
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", "q", "a"]
    while str(key) != "q":
        while not str(key) in keys:
            key = stdscr.getkey()
        stdscr.clear()
        if(key == "KEY_UP"):
            object.move(True, True)
        elif(key == "KEY_DOWN"):
            object.move(True, False)
        elif(key == "KEY_LEFT"):
            object.move(False, True)
        elif(key == "KEY_RIGHT"):
            object.move(False, False)
        elif(key == "a"):
            object.addNum()
        object.addNum()
        stdscr.addstr(object.__str__())
        stdscr.refresh()
        if(key != "q"):
            key = "-1"





wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
