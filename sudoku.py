import numpy as np
from functools import reduce
import random

# Get Data
one_hot = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1]])

data1 = np.array([[3, 0, 0, 9, 0, 0, 0, 0, 0],
                 [6, 0, 0, 0, 0, 4, 5, 7, 0],
                 [0, 0, 0, 0, 1, 0, 0, 3, 0],
                 [0, 0, 0, 0, 2, 0, 0, 0, 0],
                 [2, 0, 0, 0, 0, 0, 0, 9, 6],
                 [4, 0, 8, 0, 0, 0, 0, 0, 3],
                 [0, 0, 4, 0, 0, 0, 8, 0, 7],
                 [0, 0, 3, 0, 0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0]])

data = np.array([[3, 7, 4, 9, 1, 0, 5, 0, 0],
                 [2, 3, 0, 0, 0, 0, 0, 0, 9],
                 [0, 0, 9, 6, 0, 0, 7, 0, 2],
                 [1, 9, 0, 0, 3, 0, 0, 2, 0],
                 [0, 2, 0, 1, 0, 8, 0, 7, 0],
                 [5, 5, 0, 0, 7, 0, 0, 9, 6],
                 [7, 0, 3, 0, 0, 0, 2, 0, 1],
                 [8, 0, 0, 0, 0, 0, 0, 6, 7],
                 [0, 0, 5, 0, 2, 7, 8, 3, 0]])

class Assumption():
     def __init__(self, x, y, v, board, parent):
        self.x = x
        self.y = y
        self.v = v
        self.board = board
        self.parent = parent
        self.state = '_'
        self.child = []

        # Assign this child to the parent
        if not parent == None:
            parent.child.append(self)


ASSUMPTION_ERROR = False
# Validation Groups
ref = np.array(range(1, 10))
NULL_OPTION = np.array([0]*9)
ASSUMPTION_ERROR = False
CURR_ASSUM = Assumption(None, None, None, None ,None)


# Possibility Table
def get_options(x, y):
    global ASSUMPTION_ERROR
    union = reduce(np.union1d, (data[:, y],
                                data[x, :],
                                data[(x/3)*3:((x/3)+1)*3, (y/3)*3:((y/3)+1)*3].flatten()))
    options = np.setdiff1d(ref, union)
    options_one_hot = np.sum(one_hot[options-1], axis=0)

    if np.sum(options_one_hot) == data[x,y]:
        ASSUMPTION_ERROR = True
        print "Invalid data in board"
    return options_one_hot


def get_option_table():
    option_table = np.zeros(shape=(9, 9, 9))
    for x in range(9):
        for y in range(9):
            if data[x,y] != 0:
                option_table[x,y] = np.array([0]*9)
            else:
                option_table[x, y] = get_options(x, y)
    return option_table


def update_valid(board, option_table, x, y, v):
    union = reduce(np.union1d, (board[:, y],
                                board[x, :],
                                board[(x/3)*3:((x/3)+1)*3, (y/3)*3:((y/3)+1)*3].flatten()))
    if v in union:
        ASSUMPTION_ERROR = True
        print "*"

    elif board[x, y] == 0:
        board[x, y] = v
        #option_table[x, y] = NULL_OPTION
    return board, option_table


# Revise Possibilities
def update_definites(option_table):
    global data
    new_data = data.copy()
    for i in range(9):
        # For columns
        column = option_table[:, i]
        uniq_locs = np.where(np.sum(column, axis=1) == 1)[0]
        for l in uniq_locs:
            value = np.where(option_table[l][i] == 1)[0][0] + 1
            new_data, option_table = update_valid(new_data, option_table, l, i, value)

        uniq_vals = np.where(np.sum(column, axis=0) == 1)[0]
        for v in uniq_vals:
            idx = np.where(column[:, v] == 1)[0][0]
            new_data, option_table = update_valid(new_data, option_table, idx, i, v+1)

        # For rows
        row = option_table[i, :]
        uniq_locs = np.where(np.sum(row, axis=1) == 1)[0]
        for l in uniq_locs:
            value = np.where(option_table[i][l] == 1)[0][0] + 1
            new_data, option_table = update_valid(new_data, option_table, i, l, value)

        uniq_vals = np.where(np.sum(row, axis=0) == 1)[0]
        for v in uniq_vals:
            idx = np.where(row[:, v] == 1)[0][0]
            new_data, option_table = update_valid(new_data, option_table, i, idx, v+1)

    # For Square
    for x in range(3):
        for y in range(3):
            square = option_table[x*3:(x+1)*3, y*3:(y+1)*3].reshape(9,9)

            uniq_locs = np.where(np.sum(square, axis=1) == 1)[0]
            for l in uniq_locs:
                xid = (x*3)+(l/3)
                yid = (y*3)+(l % 3)
                value = np.where(option_table[xid][yid] == 1)[0][0] + 1
                new_data, option_table = update_valid(new_data, option_table, xid, yid, value)

            uniq_vals = np.where(np.sum(square, axis=0) == 1)[0]
            for v in uniq_vals:
                idx = np.where(square[:, v] == 1)[0][0]
                xid = (x*3)+(idx/3)
                yid = (y*3)+(idx % 3)
                new_data, option_table = update_valid(new_data, option_table, xid, yid, v+1)

    return new_data


def solve():
    global data
    while True:
        updated_data = update_definites(get_option_table())

        if ASSUMPTION_ERROR:
            return None, 1

        if not np.array_equal(updated_data, data):
            print updated_data
            #raw_input()
            data = updated_data
        elif (data == 0).any():
            return data, 0
        else:
            return None, 2


def get_assumptions(option_table):
    locs = np.argwhere(data == 0)
    idx = random.randint(0, len(locs)-1)
    x, y = locs[idx]
    values = np.where(option_table[x, y] == 1)[0] + 1
    return x, y, values


def assume(curr_data):
    global CURR_ASSUM, data, ASSUMPTION_ERROR
    parent = CURR_ASSUM
    option_table = get_option_table()
    x, y, values = get_assumptions(option_table)
    for v in values:
        print 'Assuming: ', v, 'at', x, y
        CURR_ASSUM = Assumption(x, y, v, curr_data, parent)
        data, _ = update_valid(curr_data.copy(), option_table, x, y, v)
        print 'Updated data'
        print data
        if run():
            CURR_ASSUM.state = '+'
            break
        else:
            CURR_ASSUM.state = 'x'
            print 'Assumption Invalid'
            print 'Reverting one step back'
            ASSUMPTION_ERROR = False

    return any([True for child in parent.child if child.state == '+'])


def run():
    curr_data, state = solve()
    if state == 0:
        print 'Staring to assume'
        return assume(curr_data)

    elif state == 1:
        return False

    else:
        print 'Solved your puzle buddy..!'
        return True


def run_wrapper():
    global data
    data = np.zeros(shape=(9, 9))
    for i in range(9):
        data[i] = np.array(map(int, raw_input().split(' ')))

    print "Input Data", data
    run()


if __name__ == '__main__':
    run_wrapper()
