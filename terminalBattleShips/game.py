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
        self.size = size  #playershots playerships enemyships enemyshots
        self.state = [[["≈" for i in range(size)] for j in range(size)], [["≈" for i in range(size)] for j in range(size)], [["≈" for n in range(size)] for j in range(size)], [["≈" for n in range(size)] for j in range(size)]]
        self.heatmap = [[0 for i in range(size)] for j in range(size)]
        self.score = 0
        self.mode = "placing"
        self.ships = [5, 4, 3, 3, 2]
        self.pShips = []
        self.cShips = [] # size orient location isSunk
        self.held = 0
        self.heldO = 0
        self.valid = True
        self.pWinner = None
        self.selected = [0,0]
        self.cpuMode = "run"
        self.currentTarget = [[-1, -1], 0, 0] #last hit without a sink, index of direction, length in direction
        #self.shipSigns = ["⦻ ", "▲ ", "▶ ", "▼ ", "◀ ", "■ ", "◎ ", "≈ "]
    def runAndGun(self):
        if(self.cpuMode == "run"):
            empties = []
            for i in range(self.size):
                for j in range(self.size):
                    if(self.state[3][j][i] ==  "≈" and (i+j)%2 == 0): # hit randomly in a checkerboard
                        empties.append([j,i])
            result = empties[random.randint(0, len(empties)-1)]
            _, hit, sink = self.makeShot(result, False)
            if(hit and not sink):
                self.cpuMode = "gun"
                self.currentTarget[0] = result
            else :
                self.cpuMode = "run"
        elif(self.cpuMode == "gun") :
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            loop = true
            while(loop):

                dir = directons[self.currentTarget[1]]
                dist = self.currentTarget[2]

                target = self.state[3][self.currentTarget[0][0] + dir[0]*dist][self.currentTarget[0][1] + dir[1]*dist]

                if(target == "⦻"):
                    self.currentTarget[2] += 1
                elif(target == "≈"):
                    target = target
                else:

                    if(self.currentTarget[1] <= 3):
                        self.currentTarget[1] += 1
                    else :
                        raise ValueError('A very specific bad thing happened')

        return
    def generateHeatmap(self):
        result = [[0 for i in range(self.size)] for j in range(self.size)]
        for a in range(self.size):
            for b in range(self.size):
                if self.state[3][a][b] == "≈":
                    sum = 0
                    for d in [[0,1], [0,-1], [1, 0], [-1, 0]]:
                        loop = True
                        n = 0
                        while(loop):
                            k = a + d[0]*n
                            l = b + d[1]*n
                            if(0 <= k and k < self.size and 0 <= l and l < self.size):
                                target = self.state[3][k][l]
                            else:
                                target = " "

                            if(target != "⦻" and target != "≈"):
                                loop = False
                            else:
                                if(target == "⦻"):
                                    sum += 10
                                n += 1
                            if n > 5:
                                loop = False
                        for ship in self.pShips:
                            if n >= ship[0] and not ship[3]:
                                sum += 1
                    result[a][b] = sum
                else:
                    result[a][b] = -1
        self.heatmap = result
        return
    def mayhem(self):
        top = max([max(x) for x in self.heatmap])
        empties = []
        for i in range(self.size):
            for j in range(self.size):
                if(self.state[3][j][i] ==  "≈" and self.heatmap[j][i] == top):
                    empties.append([j,i])
        result = empties[random.randint(0, len(empties)-1)]
        hit = self.makeShot(result, False)
        return
    def cpuShoot(self):
        self.generateHeatmap()
        self.mayhem()
        return
    def checkWinners(self, player):
        hits = 0
        for i in range(self.size):
            for j in range(self.size):
                if(self.state[0 if player else 3][j][i] in ["▲", "▶", "▼", "◀", "■", "⦻"]):
                    hits+=1
        if(hits == sum(self.ships)):
            self.pWinner = player
        return
    def makeShot(self, shot, player):
        result =  self.state[2 if player else 1][shot[0]][shot[1]]
        target = self.state[0 if player else 3][shot[0]][shot[1]]
        if( target == "≈"):
            hit = False
            sunk = False
            if result in ["▲", "▶", "▼", "◀", "■"]:
                hit = True
                if(player):
                    self.score += 1
                else:
                    self.score -= 1
                self.state[0 if player else 3][shot[0]][shot[1]] = "⦻"
                for n in range(len(self.cShips if player else self.pShips)):
                    ship = self.cShips[n] if player else self.pShips[n]
                    if(not ship[3]):
                        sunk = True
                        shipSqs = []
                        xDir = 1 if (ship[1] == 0) else (-1 if (ship[1] == 2) else 0)
                        yDir = 1 if (ship[1] == 1) else (-1 if (ship[1] == 3) else 0)
                        for a in range(ship[0]):
                            if not (self.state[0 if player else 3][ship[2][0] + xDir*a][ship[2][1] + yDir*a] == "⦻"):
                                sunk = False
                            shipSqs.append([ship[2][0] + xDir*a, ship[2][1] + yDir*a])
                        if sunk:
                            if(player):
                                self.score += 8-ship[0]
                            else:
                                self.score -= 10-ship[0]
                            for i in range(ship[0]):
                                part = shipSqs[i]
                                ends = ["▶", "▼", "◀", "▲"]
                                starts = ["◀", "▲", "▶", "▼"]
                                if(i == 0):
                                    self.state[0 if player else 3][part[0]][part[1]] = starts[ship[1]]
                                elif(i == ship[0]-1):
                                    self.state[0 if player else 3][part[0]][part[1]] = ends[ship[1]]
                                else:
                                    self.state[0 if player else 3][part[0]][part[1]] = "■"
                            if player:
                                self.cShips[n][3] = True
                            else:
                                self.pShips[n][3] = True
            else:
                hit = False
                self.state[0 if player else 3][shot[0]][shot[1]] = "◎"
            self.checkWinners(player)
            return True, hit, sunk
        else:
            return False, False, False
    def __str__(self, stdscr):
        falses = [False, False, False, False]
        #for i in range(self.size):
            #drawVal(stdscr, str(self.heatmap[i]) + "\n", falses)
        #for i in range(self.size):
            #drawVal(stdscr, str(self.state[3][i]) + "\n", falses)
        drawVal(stdscr, "Your Targets: " + "Your Ships:".rjust(self.size * 2 + 1) + "\n╔", falses)
        for i in range(self.size * 2 + 1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╗ ╔", falses)
        for i in range(self.size * 2 + 1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╗\n", falses)
        for i in range(self.size):
            drawVal(stdscr, "║ ", falses)
            for j in range(self.size):
                if self.selected[0] == j and self.selected[1] == i and self.mode != "placing":
                    drawVal(stdscr, self.state[0][j][i] + " ", [True, False, False, False])
                else:
                    if(self.state[0][j][i] in ["▲", "▶", "▼", "◀", "■"]):
                        drawVal(stdscr, self.state[0][j][i] + " ", [False, False, False, True])
                    else:
                        drawVal(stdscr, self.state[0][j][i] + " ", falses)
            drawVal(stdscr, "║ ║ ", falses)
            for j in range(self.size):
                if(self.mode == "placing"):
                    ship = []
                    xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
                    yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
                    for n in range(self.ships[self.held]):
                        ship.append([self.selected[0] + xDir*n, self.selected[1] + yDir*n])
                    if [j,i] in ship:
                        ends = ["▶ ", "▼ ", "◀ ", "▲ "]
                        starts = ["◀ ", "▲ ", "▶ ", "▼ "]
                        if(ship.index([j,i]) == 0):
                            drawVal(stdscr, starts[self.heldO], [True, True, self.valid, False])
                        elif(ship.index([j,i]) == len(ship)-1):
                            drawVal(stdscr, ends[self.heldO], [True, True, self.valid, False])
                        else:
                            drawVal(stdscr, "■ ", [True, True, self.valid, False])
                    else:
                        drawVal(stdscr, self.state[1][j][i] + " ", falses)
                else:
                    hit = self.state[3][j][i] in ["⦻", "▲", "▶", "▼", "◀", "■", "◎"]
                    if(hit):
                        if(self.state[3][j][i] == "◎"):
                            drawVal(stdscr, self.state[3][j][i] + " ", [False, False, False, True])
                        else:
                            drawVal(stdscr, self.state[1][j][i] + " ", [False, False, False, True])
                    else:
                        drawVal(stdscr, self.state[1][j][i] + " ", falses)
            drawVal(stdscr, "║\n", falses)
        drawVal(stdscr, "╚", falses)
        for i in range(self.size * 2 +1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╝ ╚", falses)
        for i in range(self.size * 2 +1):
            drawVal(stdscr, "═", falses)
        drawVal(stdscr, "╝\n", falses)
        return
    def placeComputerShips(self):
        for n in range(len(self.ships)):
            valid = False
            while not valid:
                cpuHeldO = random.randint(0, 3)
                cpuSelected = [random.randint(0, self.size-1),random.randint(0, self.size-1)]
                ship = []
                xDir = 1 if (cpuHeldO == 0) else (-1 if (cpuHeldO == 2) else 0)
                yDir = 1 if (cpuHeldO == 1) else (-1 if (cpuHeldO == 3) else 0)
                for a in range(self.ships[n]):
                    ship.append([cpuSelected[0] + xDir*a, cpuSelected[1] + yDir*a])
                valid = checkValid(self.state[2], ship)
            for i in range(len(ship)):
                part = ship[i]
                ends = ["▶", "▼", "◀", "▲"]
                starts = ["◀", "▲", "▶", "▼"]
                if(i == 0):
                    self.state[2][part[0]][part[1]] = starts[cpuHeldO]
                elif(i == len(ship)-1):
                    self.state[2][part[0]][part[1]] = ends[cpuHeldO]
                else:
                    self.state[2][part[0]][part[1]] = "■"
            self.cShips.append([self.ships[n], cpuHeldO, cpuSelected, False])

    def placeHeld(self):
        ship = []
        xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
        yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
        for n in range(self.ships[self.held]):
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
        self.pShips.append([self.held, self.heldO, self.selected, False])
        if self.held < len(self.ships)-1:
            self.held = self.held + 1
        else:
            self.mode = "playing"
            self.placeComputerShips()
        self.selected = [0,0]
        self.updateValid()
    def updateValid(self):
        ship = []
        xDir = 1 if (self.heldO == 0) else (-1 if (self.heldO == 2) else 0)
        yDir = 1 if (self.heldO == 1) else (-1 if (self.heldO == 3) else 0)
        for n in range(self.ships[self.held]):
            ship.append([self.selected[0] + xDir*n, self.selected[1] + yDir*n])
        self.valid = checkValid(self.state[1], ship)

def checkValid(state, ship):
    result = True
    size = len(state[0])
    for i in range(len(ship)):
        part = ship[i]
        if(part[0] <= -1 or part[0] >= size or part[1] <= -1 or part[1] >= size):
            result = False
        elif state[part[0]][part[1]] in ["▲", "▶", "▼", "◀", "■"]:
            result = False
    return result

def drawVal(stdscr, val, bools): # w r g b c y
    selected, placing, valid, sunk = bools
    col = curses.color_pair(1)
    if placing:
        if valid:
            col = curses.color_pair(3)
        else :
            col = curses.color_pair(2)
    else:
        if val == "⦻ ":
            col = curses.color_pair(2)
        elif val == "≈ ":
            col = curses.color_pair(4)
        elif val == "◎ ":
            col = curses.color_pair(5)
        else:
            col = curses.color_pair(1)
        if selected:
            col = curses.color_pair(1)
        if sunk and not val == "◎ ":
            col = curses.color_pair(2)
    stdscr.addstr(val, col)

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
        elif object.mode == "playing":
            success, _, _ = object.makeShot(object.selected, True)
            if(success):
                object.cpuShoot()
        else:
            object.updateValid()
    elif(key == "r" or key=="s" or key=="m" or key=="l"):
        x = object.size * 2 + 30
        if key == "s":
            boardSize = 8
        elif key == "m":
            boardSize = 10
        elif key == "l":
            boardSize = 12
        object = Board(boardSize)
        pause = False
        x = object.size * 2 + 32
        rows, cols = stdscr.getmaxyx()
        info = curses.newwin(25, cols-x, 0, x)
    object.__str__(stdscr)
    info.clear()
    info.addstr(getInfo(object))
    if(object.pWinner != None):
        pause = True
        if(object.score > int(hScore)):
            updateHScore(object.score)
            hScore = object.score
    stdscr.addstr("\n\nYour Score: " + str(object.score) +'\n')
    stdscr.addstr("High Score: " + str(hScore) +'\n')
    stdscr.refresh()
    info.refresh()

    if(key != "q"):
        key = "-1"
    return key, object, pause, hScore, boardSize, info

def getInfo(object):
    result = "Welcome to BattleShips!\n"
    if(object.pWinner == None):
        if(object.mode == "placing"):
            result += "Place your ships!\n"
            result += "Use Arrowkeys to move\n"
            result += "Use Space to Rotate\n"
            result += "Use Return to confirm\n"
        else :
            result += "Choose your target!\n"
            result += "Use Arrowkeys to move\n"
            result += "Use Return to confirm\n"
    else:
        result += "\nYou " + ("Win!\n" if object.pWinner else "Lose!\n")
    result += "\nUse the 'R' key to reset\n"
    result += "Use the 'Q' key to quit\n"
    result += "Use the 'S','M' and 'L' keys\n"
    result += "to change the size of the board\n"

    return result

def main(stdscr):           #main function is entry point to game
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    hScore = readHScore()
    # Clear screen
    stdscr.clear()
    boardSize = 10
    object = Board(boardSize)
    object.__str__(stdscr)
    rows, cols = stdscr.getmaxyx()
    x = object.size * 2 + 30
    info = curses.newwin(25, cols-x, 0, x)

    pause = False
    keys = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT", " ", "\n", "q", "r", "s", "m", "l"]
    info.clear()
    info.addstr(getInfo(object))
    stdscr.refresh()
    info.refresh()
    key = stdscr.getkey()
    while str(key) != "q":
        key, object, pause, hScore, boardSize, info = gameLoop(stdscr, info, key, keys, object, pause, hScore, boardSize)

wrapper(main)               #wrapper catches exceptions, closes curses and then prints exceptions


curses.nocbreak()           #terminate curses commands
stdscr.keypad(False)
curses.echo()
curses.endwin()
