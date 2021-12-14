# Built-in modules
import logging

import numpy

# Local modules
from sudoker import utils


class DecisionTree(object):
    '''
    Tracks search space and state at each branch
    '''
    def __init__(self, state=None, previous_decision=None):
        self.state = state
        self.parent = previous_decision
        self.child = []
        if self.parent is not None:
            self.parent.child.append(self)


class Search(object):
    '''
    Chooses the next move for the solver
    Goes deeper if the move is valid
    Revert back the state if the chosen move results in invalid state
    '''

    def __init__(self, Solver):
        self.Solver = Solver
        self.solutions = []
        self.log = logging.getLogger('Search')

    def search(self, state, previous_decision=DecisionTree()):
        state, possible_states, is_valid = self.Solver.solve(state)

        if not is_valid:
            return

        if possible_states is None:
            self.solutions.append(state)
            self.log.info('Solution: \n%s', utils.get_pretty_board(state))
            self.solutions.append(state)
            return

        # Explore the possible states
        for chosen_state in possible_states:
            current_decision = DecisionTree(chosen_state, previous_decision)
            self.search(chosen_state, current_decision)