'''
Provides all possible solution for the incomplete 9x9 sudoku board
'''

# Built-in modules
from functools import reduce
import random
import copy

# External packages
import numpy as np

# Local modules
from search import Search
import utils


class SudokuSolver(object):
    def __init__(self):
        self.log = logging.getLogger('Solver')

    def solve(self, state):
        '''
        Solve untill the decisions are certain and valid
        '''
        self.is_valid = True
        while True:
            updated_state = self.update_definites(
                    self.get_option_table(state), state)

            if not self.is_valid:
                return state, None, False
            
            if np.array_equal(updated_state, state):  # is the board modified ? 
                if (state == 0).any():  # is there any empty cells?
                    return state, self.possible_states(updated_state), True
                else:
                    return state, None, True

            state = updated_state

    def update_definites(self, option_table, state):
        '''
        Update all the certain decision w.r.t the current state of the board
        Scan Column wise, Row wise and 3x3 square wise (as humans do while solving)
        '''
        new_data = copy.deepcopy(state)
        for i in range(9):
            # Fill by column
            column = option_table[:, i]
            uniq_locs = np.where(np.sum(column, axis=1) == 1)[0]
            for l in uniq_locs:
                value = np.where(option_table[l][i] == 1)[0][0] + 1
                new_data, option_table = self.update(
                        new_data, option_table, l, i, value)

            uniq_vals = np.where(np.sum(column, axis=0) == 1)[0]
            for v in uniq_vals:
                idx = np.where(column[:, v] == 1)[0][0]
                new_data, option_table = self.update(
                        new_data, option_table, idx, i, v+1)

            # Fill by row 
            row = option_table[i, :]
            uniq_locs = np.where(np.sum(row, axis=1) == 1)[0]
            for l in uniq_locs:
                value = np.where(option_table[i][l] == 1)[0][0] + 1
                new_data, option_table = self.update(
                        new_data, option_table, i, l, value)

            uniq_vals = np.where(np.sum(row, axis=0) == 1)[0]
            for v in uniq_vals:
                idx = np.where(row[:, v] == 1)[0][0]
                new_data, option_table = self.update(
                        new_data, option_table, i, idx, v+1)

        # Fill all the 3x3 squares
        for x in range(3):
            for y in range(3):
                square = option_table[x*3:(x+1)*3, y*3:(y+1)*3].reshape(9, 9)

                uniq_locs = np.where(np.sum(square, axis=1) == 1)[0]
                for l in uniq_locs:
                    xid = (x*3)+(l/3)
                    yid = (y*3)+(l % 3)
                    value = np.where(option_table[xid][yid] == 1)[0][0] + 1
                    new_data, option_table = self.update(
                            new_data, option_table, xid, yid, value)

                uniq_vals = np.where(np.sum(square, axis=0) == 1)[0]
                for v in uniq_vals:
                    idx = np.where(square[:, v] == 1)[0][0]
                    xid = (x*3)+(idx/3)
                    yid = (y*3)+(idx % 3)
                    new_data, option_table = self.update(
                            new_data, option_table, xid, yid, v+1)

        return new_data

    def get_invalid_entries(self, state, x, y):
        ''' 
        Gets all the invalid entries for the given cell
        '''
        entries_along_row = state[:, y]
        entries_along_column = state[x, :]
        entries_within_3x3 = state[(x/3)*3:((x/3)+1)*3,
                (y/3)*3:((y/3)+1)*3].flatten()
        invalid_entries = list(reduce(np.union1d, (entries_along_row,
            entries_along_column, entries_within_3x3)))
        return invalid_entries

    def update(self, state, option_table, x, y, v):
        '''
        Updates the values v at the given cell (x,y)
        if it obeys the rules of the game
        '''
        
        invalid_entries = self.get_invalid_entries(state, x, y)

        if state[x, y] in invalid_entries:
            invalid_entries.remove(state[x, y])
            
        if v in invalid_entries:
            self.is_valid = False
            self.log.debug("Invalid state in board")

        elif state[x, y] == 0:
            state[x, y] = v
            
        return state, option_table

    def possible_states(self, state):
        '''
        Generates outcomes of the possible moves
        '''
        option_table = self.get_option_table(state)
        x, y, values = self.next_moves(option_table)

        return [self.update(state.copy(), option_table, x, y, v)[0]
                for v in values]

    def get_possible_moves(self, x, y, state):
        ''' 
        Gets all the possible moves at a given cell (x, y) for the give state
        '''
        invalid_entries = self.get_invalid_entries(state, x, y)
        options = np.setdiff1d(ref, invalid_entries)
        options_one_hot = np.sum(one_hot[options-1], axis=0)
    
        if np.sum(options_one_hot) == state[x, y]:
            # self.is_valid = False
            self.log.debug("Invalid state in board")
        return options_one_hot
    
    
    def get_option_table(self, state):
        '''
        Populates the entire table with all possible moves at each empty cell
        '''
        option_table = np.zeros(shape=(9, 9, 9))
        for x in range(9):
            for y in range(9):
                if state[x, y] != 0:
                    option_table[x, y] = np.array([0]*9)
                else:
                    option_table[x, y] = self.get_possible_moves(x, y, state)
        return option_table


    def next_moves(self, option_table):
        '''
        Randomly chooses an empty cell to continue solving
        '''
        locs = np.argwhere(data == 0)
        idx = random.randint(0, len(locs)-1)
        x, y = locs[idx]
        values = np.where(option_table[x, y] == 1)[0] + 1
        return x, y, values


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', type=str,
            default='input.txt', help='input file path')
    parser.add_argument('-o', '--output-file', type=str,
            default='output.txt', help='output file path')
    args = parser.parse_args()

    import logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('Board')

    ref = np.array(range(1, 10))
    one_hot = np.eye(9)

    # Gets board data from input file
    with open(args.input_file, 'r') as input_file:
        table_data_str = input_file.readlines()
    data = np.zeros(shape=(9, 9))
    for i, row_str in zip(range(9), table_data_str):
        data[i] = np.array(map(int, row_str.strip().split(' ')))
    log.info('Input board: \n%s', utils.get_pretty_board(data))

    solver = Search(SudokuSolver())
    solver.search(data)
    log.info('Number of possible solutions: %d', len(solver.solutions))
