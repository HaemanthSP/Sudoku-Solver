# Sudoku Solver - 9x9

The project targets at finding the all possible solutions to complete the given 9x9 sudoku board.
The project has two major modules:
1. Solve - Defines the guideline and the logic to solve the game
2. Search - Searches through all possible combinations to satisfy the solver. This module to completely abstracted from the game.


## Module definition:

SudokuSolver <--> Search

Solver module: 
1. Should validate the given state
2. Should provide all possible moves at an instance

Search module:
1. Should choose the next move from the possible moves
2. Should go deeper when the move is valid
3. Should backtrack when the state of the board becmones invalid


## Input

Create an `input.txt` file with sudoku 9x9 puzzle
Create a grid of space speparated values use '0' for empty cells
```
For example:
4 0 0 8 0 0 7 0 0
0 0 0 9 0 0 0 8 0
0 0 0 0 6 0 9 0 3
0 0 1 5 0 0 0 7 0
0 6 0 1 0 4 0 5 0
0 5 0 0 0 3 1 0 0
3 0 2 0 1 0 0 0 0
0 9 0 0 0 7 0 0 0
0 0 8 0 0 6 0 0 7
```

## Usage
```
python sudoku.py
```

# Output
```
INFO:Board:Input board: 
4 0 0 8 0 0 7 0 0
0 0 0 9 0 0 0 8 0
0 0 0 0 6 0 9 0 3
0 0 1 5 0 0 0 7 0
0 6 0 1 0 4 0 5 0
0 5 0 0 0 3 1 0 0
3 0 2 0 1 0 0 0 0
0 9 0 0 0 7 0 0 0
0 0 8 0 0 6 0 0 7
INFO:Search:Solution: 
4 2 9 8 3 5 7 6 1
7 3 6 9 4 1 5 8 2
1 8 5 7 6 2 9 4 3
8 4 1 5 2 9 3 7 6
2 6 3 1 7 4 8 5 9
9 5 7 6 8 3 1 2 4
3 7 2 4 1 8 6 9 5
6 9 4 3 5 7 2 1 8
5 1 8 2 9 6 4 3 7
INFO:Board:Number of possible solutions: 1
```
