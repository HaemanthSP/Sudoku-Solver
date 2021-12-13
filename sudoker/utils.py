'''
Utility functions
'''

# External modules
import numpy as np


def read_input_from_file(file_name):
    '''
    Reads the board input of specified form from a file
    '''
    with open(file_name, 'r') as input_file:
        table_data_str = input_file.readlines()
    data = np.zeros(shape=(9, 9))
    for i, row_str in zip(range(9), table_data_str):
        clean_str = row_str.strip().split(' ')
        int_list = list(map(int, clean_str))
        data[i] = np.array(int_list)
    return data


def get_pretty_board(data):
    '''
    Converts the board data from numpy array to string
    '''
    row_str = [' '.join(list(map(lambda x: str(int(x)), data_row)))
            for data_row in data]
    return '\n'.join(row_str)
