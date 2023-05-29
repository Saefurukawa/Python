"""
Sae Furukawa
CS51-02 assignment 10
April 17th, 2022
"""

"""
experiment 1
With the best first search, it took 0.07 second. With the uninformed search, it took 0.56 second. This proves the 
efficiency of the best first search method. The informed search performs faster than the uninformed search because it 
knows what the solution looks like and it always tries to get closer to the goal state while the uninformed search takes 
into account all possible next states.           

experiment 2
With the propagate function, it took only 0.02 second. The propagate function speeds up the process because it iterates 
through each entry in the next_state to find the domain with the only possible input and check if such an input is possible.
Thus, the propagate function speeds up the process by looking ahead in steps.

"""

import copy
import time

class SudokuState:
    """
    Class: SudokuState: play n * n Sudoku problem
    Instance Variables: self.size: the size of Sudoku
                        self.num_placed: the number of numbers placed
                        self.board: the current state of the board
    """

    def __init__(self):
        """
        Constructor
        return: none
        """
        self.size = 9
        self.num_placed = 0
        self.board = []

        # construct the empty board
        for i in range(self.size):
            list = []
            for j in range(self.size):
                list.append(SudokuEntry())
            self.board.append(list)

    def get_subgrid_number(self, row, col):
        """
        Returns a number between 1 and 9 representing the subgrid
        that this row, col is in.  The top left subgrid is 1, then
        2 to the right, then 3 in the upper right, etc.
        """
        row_q = int(row / 3)
        col_q = int(col / 3)
        return row_q * 3 + col_q + 1

    def get_any_available_cell(self):
        """
        An uninformed cell finding variant.  If you use
        this instead of find_most_constrained_cell
        the search will perform a depth first search.
        """
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c].is_fixed():
                    return r,c
        return None

    def propagate(self):
        for ri in range(self.size):
            for ci in range(self.size):
                if not self.board[ri][ci].is_fixed() and \
                   self.board[ri][ci].width() == 1:
                    self.add_number(ri, ci, self.board[ri][ci].values()[0])
                    if self.solution_is_possible():
                        self.propagate()
                        return

    def get_raw_string(self):
        """
        get a raw data
        :return: string representing a raw data of Sudoku state
        """
        board_str = ""

        for r in self.board:
            board_str += str(r) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_str

    def remove_conflict(self, row, column, number):
        """
        Remove a number from the list of possible numbers for that entry
        :param row: a row of the entry
        :param column: a column of the entry
        :param number: a number to be removed
        :return: none
        """
        if not self.board[row][column].is_fixed():
            self.board[row][column].eliminate(number)

    def remove_all_conflicts(self, row, column, number):
        """
        Remove a number from the same row, column, and subgrid
        :param row: a row of the entry
        :param column: a column of the entry
        :param number: the number to be removed
        :return: none
        """

        #delete the number from the same row
        for i in range(self.size):
            self.remove_conflict(row, i, number)

        #delete the number from the same column
        for j in range(self.size):
            self.remove_conflict(j, column, number)

        # Check all conditions for subgrid
        subgrid = self.get_subgrid_number(row, column)
        
        if subgrid == 1:
            for i in range(3):
                for j in range(3):
                        self.remove_conflict(i, j, number)

        elif subgrid == 2:
            for i in range(3):
                for j in range(3,6):
                    self.remove_conflict(i, j, number)

        elif subgrid == 3:
            for i in range(3):
                for j in range(6, 9):
                    self.remove_conflict(i, j, number)

        elif subgrid == 4:
            for i in range(3,6):
                for j in range(3):
                    self.remove_conflict(i, j, number)

        elif subgrid == 5:
            for i in range(3,6):
                for j in range(3, 6):
                    self.remove_conflict(i, j, number)

        elif subgrid == 6:
            for i in range(3,6):
                for j in range(6, 9):
                    self.remove_conflict(i, j, number)

        elif subgrid == 7:
            for i in range(6,9):
                for j in range(3):
                    self.remove_conflict(i, j, number)

        elif subgrid == 8:
            for i in range(6,9):
                for j in range(3, 6):
                    self.remove_conflict(i, j, number)

        elif subgrid == 9:
            for i in range(6, 9):
                for j in range(6, 9):
                    self.remove_conflict(i, j, number)


    def add_number(self, row, column, number):
        """
        Add a number to the empty entry
        :param row: a row of the entry
        :param column: a column of the entry
        :param number: a number
        :return: none
        """
        self.board[row][column].fix(number)
        self.remove_all_conflicts(row, column, number)
        self.num_placed += 1

    def get_most_constrained_cell(self):
        """
        Find the cell with the least number of possible solutions
        :return: a tuple representing a row and column of the most constrained cell
        """
        option = self.size
        most_constrained = (-1,-1)

        # Find the entry with the least number of possible numbers
        for r in range(self.size):
            for c in range(self.size):

                #check if the entry is still empty
                if not self.board[r][c].is_fixed():
                    if option > self.board[r][c].width():
                        option = self.board[r][c].width()
                        most_constrained = (r,c)

        return most_constrained

    def solution_is_possible(self):
        """
        Check if the solution is possible
        :return: Boolean representing whether the solution is possible
        """

        # Find any unfixed cell and check if they have at least one possible number to put in
        for r in range(self.size):
            for c in range(self.size):

                #check if the entry is still empty
                if not self.board[r][c].is_fixed():
                    if self.board[r][c].width() == 0:
                        return False

        return True

    def next_states(self):
        """
        Return a list of possible next states based on the current state
        :return: a list representing possible next states
        """
        next_states = []

        (r,c) = self.get_most_constrained_cell()

        #Go through every possible number in the cell and check if the solution is possible
        for number in self.board[r][c].values():
            new_state = copy.deepcopy(self)

            # add a number and create a new state
            new_state.add_number(r, c, number)

            # check if the state is possible
            if new_state.solution_is_possible():
                next_states.append(new_state)

        return next_states

    def is_goal(self):
        """
        Check if this is a goal state
        :return: boolean representing whether it's a goal state
        """

        return self.num_placed == self.size * self.size

    def __str__(self):
        """
        prints all numbers assigned to cells.  Unassigned cells (i.e.
        those with a list of options remaining are printed as blanks
        """
        board_string = ""

        for r in range(self.size):
            if r % 3 == 0:
                board_string += " " + "-" * (self.size * 2 + 5) + "\n"

            for c in range(self.size):
                entry = self.board[r][c]

                if c % 3 == 0:
                    board_string += "| "

                board_string += str(entry) + " "

            board_string += "|\n"

        board_string += " " + "-" * (self.size * 2 + 5) + "\n"

        return "num placed: " + str(self.num_placed) + "\n" + board_string


# -----------------------------------------------------------------------
# Make all of your changes to the SudokuState class above.
# only when you're running the last experiments will
# you need to change anything below here and then only
# the different problem inputs

class SudokuEntry:
    def __init__(self):
        self.fixed = False
        self.domain = list(range(1, 10))

    def is_fixed(self):
        return self.fixed

    def width(self):
        return len(self.domain)

    def values(self):
        return self.domain

    def has_conflict(self):
        return len(self.domain) == 0

    def __str__(self):
        if self.fixed:
            return str(self.domain[0])
        return "_"

    def __repr__(self):
        if self.fixed:
            return str(self.domain[0])
        return str(self.domain)

    def fix(self, n):
        assert n in self.domain
        self.domain = [n]
        self.fixed = True

    def eliminate(self, n):
        if n in self.domain:
            assert not self.fixed
            self.domain.remove(n)

# -----------------------------------
# Even though this is the same DFS code
# that we used last time, our next_states
# function is makeing an "informed" decision
# so this algorithm performs similarly to
# best first search.


def dfs(state):
    """
    Recursive depth first search implementation

    Input:
    Takes as input a state.  The state class MUST have the following
    methods implemented:
    - is_goal(): returns True if the state is a goal state, False otherwise
    - next_states(): returns a list of the VALID states that can be
    reached from the current state

    Output:
    Returns a list of ALL states that are solutions (i.e. is_goal
    returned True) that can be reached from the input state.
    """
    # if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        # make a list to accumulate the solutions in
        result = []

        for s in state.next_states():
            result += dfs(s)

        return result

# ------------------------------------
# three different board configurations:
# - problem1
# - problem2
# - heart (example from class notes)


def problem1():
    b = SudokuState()
    b.add_number(0, 1, 7)
    b.add_number(0, 7, 1)
    b.add_number(1, 2, 9)
    b.add_number(1, 3, 7)
    b.add_number(1, 5, 4)
    b.add_number(1, 6, 2)
    b.add_number(2, 2, 8)
    b.add_number(2, 3, 9)
    b.add_number(2, 6, 3)
    b.add_number(3, 1, 4)
    b.add_number(3, 2, 3)
    b.add_number(3, 4, 6)
    b.add_number(4, 1, 9)
    b.add_number(4, 3, 1)
    b.add_number(4, 5, 8)
    b.add_number(4, 7, 7)
    b.add_number(5, 4, 2)
    b.add_number(5, 6, 1)
    b.add_number(5, 7, 5)
    b.add_number(6, 2, 4)
    b.add_number(6, 5, 5)
    b.add_number(6, 6, 7)
    b.add_number(7, 2, 7)
    b.add_number(7, 3, 4)
    b.add_number(7, 5, 1)
    b.add_number(7, 6, 9)
    b.add_number(8, 1, 3)
    b.add_number(8, 7, 8)
    return b


def problem2():
    b = SudokuState()
    b.add_number(0, 1, 2)
    b.add_number(0, 3, 3)
    b.add_number(0, 5, 5)
    b.add_number(0, 7, 4)
    b.add_number(1, 6, 9)
    b.add_number(2, 1, 7)
    b.add_number(2, 4, 4)
    b.add_number(2, 7, 8)
    b.add_number(3, 0, 1)
    b.add_number(3, 2, 7)
    b.add_number(3, 5, 9)
    b.add_number(3, 8, 2)
    b.add_number(4, 1, 9)
    b.add_number(4, 4, 3)
    b.add_number(4, 7, 6)
    b.add_number(5, 0, 6)
    b.add_number(5, 3, 7)
    b.add_number(5, 6, 5)
    b.add_number(5, 8, 8)
    b.add_number(6, 1, 1)
    b.add_number(6, 4, 9)
    b.add_number(6, 7, 2)
    b.add_number(7, 2, 6)
    b.add_number(8, 1, 4)
    b.add_number(8, 3, 8)
    b.add_number(8, 5, 7)
    b.add_number(8, 7, 5)
    return b


def heart():
    b = SudokuState()
    b.add_number(1, 1, 4)
    b.add_number(1, 2, 3)
    b.add_number(1, 6, 6)
    b.add_number(1, 7, 7)
    b.add_number(2, 0, 5)
    b.add_number(2, 3, 4)
    b.add_number(2, 5, 2)
    b.add_number(2, 8, 8)
    b.add_number(3, 0, 8)
    b.add_number(3, 4, 6)
    b.add_number(3, 8, 1)
    b.add_number(4, 0, 2)
    b.add_number(4, 8, 5)
    b.add_number(5, 1, 5)
    b.add_number(5, 7, 4)
    b.add_number(6, 2, 6)
    b.add_number(6, 6, 7)
    b.add_number(7, 3, 5)
    b.add_number(7, 5, 1)
    b.add_number(8, 4, 8)
    return b


# --------------------------------
# Code that actual runs a sudoku problem, times it
# and prints out the solution.
# You can vary which problem your running on between
# problem1(), problem2() and heart() by changing the line
# below
#
# Uncomment this code when you have everything implemented and you
# want to solve some of the sample problems!

#problem = heart()
#print("Starting board:")
#print(problem)

#start_time = time.time()
#solutions = dfs(problem)
#search_time = time.time()-start_time

#print("Search took " + str(round(search_time, 2)) + " seconds")
#print("There was " + str(len(solutions)) + " solution.\n\n")
#if len(solutions) > 0:
    #print(solutions[0])
