class Assumption(object):
    def __init__(self, state, previous_assumption):
        self.state = state
        self.parent = previous_assumption
        self.child = []
        if self.parent is not None:
            self.parent.child.append(self)


class Search(object):
    def __init__(self, Solver):
        self.Solver = Solver
        self.assumption = Assumption(state=None, previous_assumption=None)
        self.solutions = []

    def search(self, state):
        return self.__search(state, self.assumption)

    def __search(self, state, previous_assumption):
        possible_states, is_valid = self.Solver.solve(state)
        if not is_valid:
            return

        # Explore the possible states
        for current_state in possible_states:
            current_assumption = Assumption(current_state, previous_assumption)
            self.__search(current_state, current_assumption)
        else:
            self.solutions.append(state)
