Module definition:
------------------

SudokuSolver <--> Search

Solver module(Defines the games's rules and moves): 
1. Should validate the given state
2. Should provide all possible moves at an instance

Search module(Abstracted from Sudoku; Should be compatible with other games):
1. Should choose the next move from the possible moves
2. Should go deeper when the move is valid
3. Should backtrack when the state of the board becmones invalid


Input.txt
---------
Enter the space separated enries of 9x9 table
Replace the empty cell with '0'


Execution:
----------
python sudoku.py
