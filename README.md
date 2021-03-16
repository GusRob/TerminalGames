# TerminalGames
Simple games to play in the terminal using the 'curses' screen and keyboard handling library in python

## This repository will consist of a series of Terminal minigames
*  - [X] 2048 block sliding game
*  - [X] Noughts and Crosses
*  - [ ] Tetris
*  - [X] Battleships
*  - [X] Snake
*  - [ ] Greed

#### Opponents
*  - [ ] Noughts and Crosses
*  - [ ] Battleships

## Usage Instructions

  * To run the minigame interface, the 'termGame' file can be executed as any other executable file with the name of the game to play as an argument due to it's shebang addition, allowing the user to call, for example './termGame 2048' to launch the 2048 game
  * The CLI can be run without arguments, with the name of the game as an argument, or the name of the game as an optional argument flag
    * ```./termGame```
    * ```./termGame snake```
    * ```./termGame --snake```
  * To exit games and return to the termGame CLI, the user should press the 'Q' key and to run games from within the CLI, the user only needs to type the name of the game and press return
  * To exit the CLI, the user should run the command 'quit'
  * For a full list of commands, the user should run the command 'help'

## Milestone Log

2021/03/10
  * Python terminal window updating process implemented with curses
  * Basic board printing and movement capabilities implemented for 2048 game
  * Some bugs with combining squares yet to be fixed

2021/03/11
  * 2048 game mechanics now complete
  * Additional information window needs instructions on how to play added
  * TermGame launcher has help features and requests commands on a loop until quit
  * Yet to implement
    * Instructions on how to play
    * Additional games

2021/03/12
  * Os and Xs game engine fully implemented
  * Basic opponent added that will play wins and block losses where possible, does not compute any turns ahead
  * Need to decide how to develop opponent algorithm, brief research gives two main options;
    * Minimax algorithm, would be flexible if i decide to develop game further
    * Newell and Simon's 1972 tic-tac-toe program rules, need to look into the reasoning for moves further but could be less memory intensive/more efficient
  * Next game to implement in the meantime will be battleships

 2021/03/13
  * Battleships game engine completely implemented
  * Basic opponent added that will shoot randomly always
  * Next steps to develop the battleship opponent algorithm
    * Once bot scores a hit, they should change strategy and start shooting round the hit
    * When searching for initial hit, attack grid in a checkered mask in order to reduce useless shots
    * A more advanced algorithm could map a probability calculating function to every square on the board in order to choose squares with most possible ship placements over them
  * Next game to implement in the meantime will be tetris

2021/03/16
  * Snake game implemented
  * Chose to implement this before the tetris game, as it is simpler and adjusting the previous game format to use a timer was easier with this game
  * Instead of the game waiting for a keypress and then state updating, the game runs a loop every 0.05 seconds
  * A move counter increments to keep track of the game speed
  * The only problem with this approach is that if the computer runs slowly, e.g. th computer is processor has lots of background tasks, then the game will slow down rapidly, as the state will not update asynchronously
