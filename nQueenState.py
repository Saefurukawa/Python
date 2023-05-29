 """
Sae Furukawa
CS51-02 assignment 9
April 10, 2022
"""
# code for you class goes here
import copy

class NQueenState:
    """
    NQueenState: class playing N Queen problem
    Instance Variables: self.size: a size of board
                        self.num_queens_placed: a number of queens placed
                        self.board: a board representing a current state
    """
    def __init__(self, size):
        """
        Constructor
        :param size: a size of board
        return: none
        """
        self.size = size
        self.num_queens_placed = 0
        self.board = []

        #create an initial state
        for i in range(size):
            self.board.append([0] * size)


    def is_valid_move(self, row, column):
        """
        Check if the move is valid
        :param row: a row that we are trying to put a queen on
        :param column: a column that we are trying to put a queen on
        :return: True if valid, False if not valid
        """

        return self.count_queen() and self.queen_space(row, column) and self.check_conflict(row, column)


    def count_queen(self):
        """
        Count a number of queens on the board
        :return: True if the number of queens does not equal the size, else false
        """
        count_queen = 0

        #count the number of queens
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    count_queen += 1

        return not count_queen == self.size


    def queen_space(self, row, column):
        """
        Check if the queen is already on at the place
        :param row: a row that we are trying to put a queen on
        :param column: a column that we are trying to put a queen on
        :return: False if it's already there, True otherwise
        """
        return not self.board[row][column] == 1

    def check_conflict(self, row, column):
        """
        Check if any queen is on diagonal
        :param row: a row that we are trying to put a queen on
        :param column: a column that we are trying to put a queen on
        :return:
        """

        #check the same row and column
        for i in range(self.size):
            if self.board[row][i] == 1:
                return False

            elif self.board[i][column] == 1:
                return False

        r_marker = row
        c_marker = column

        #go to the right upper corner
        while 0 <= r_marker < self.size and 0 <= c_marker < self.size:
            r_marker -= 1
            c_marker += 1

            if 0 <= r_marker < self.size and 0 <= c_marker < self.size:
                if self.board[r_marker][c_marker] == 1:
                    return False

        r_marker = row
        c_marker = column

        # go to the right lower corner
        while 0 <= r_marker < self.size and 0 <= c_marker < self.size:
            r_marker += 1
            c_marker -= 1

            if 0 <= r_marker < self.size and 0 <= c_marker < self.size:
                if self.board[r_marker][c_marker] == 1:
                    return False

        r_marker = row
        c_marker = column

        # go to the right lower corner
        while 0 <= r_marker < self.size and 0 <= c_marker < self.size:
            r_marker += 1
            c_marker += 1

            if 0 <= r_marker < self.size and 0 <= c_marker < self.size:
                if self.board[r_marker][c_marker] == 1:
                    return False

        r_marker = row
        c_marker = column

        # go to the right lower corner
        while 0 <= r_marker < self.size and 0 <= c_marker < self.size:
            r_marker -= 1
            c_marker -= 1

            if 0 <= r_marker < self.size and 0 <= c_marker < self.size:
                if self.board[r_marker][c_marker] == 1:
                    return False

        return True

    def add_queen(self, row, column):
        """
        Create the new state by putting the queen on the stop
        :param row: a row that we are trying to put a queen on
        :param column: a column that we are trying to put a column on
        :return: new_state: a copy of the state
        """
        new_state = copy.deepcopy(self)
        new_state.board[row][column] = 1

        new_state.num_queens_placed += 1

        return new_state

    def next_states(self):
        """
        Return a list of next states based on the current state
        :return: next_states: a list of next states
        """
        next_states = []

        #find the next empty row and check valid moves
        for r in range(self.size):
            if 1 not in self.board[r]:
                for c in range(self.size):
                    if self.is_valid_move(r, c):
                        next_states.append(self.add_queen(r, c))

                break

        return next_states

    def is_goal(self):
        """
        Check if the current state is a goal state
        :return: True if it's a goal state, False otherwise
        """
        return self.num_queens_placed == self.size

    def __str__(self):
        """
        Print out the state of the board
        :return: board_string: a string representing statement
        """
        board_string = "Board size: " + str(self.size)+ "\n" +  "Number of queens placed: " + str(self.num_queens_placed)

        board_string += "\n"

        #print a row one by one
        for i in range(self.size):
            board_string += str(self.board[i]) + "\n"

        return board_string


def dfs(state):
    """Recursive depth first search implementation
    
    Input:
    Takes as input a state.  The state class MUST have the following
    returned True) that can be reached from the input state.
    """
    
    #if the current state is a goal state, then return it in a list
    if state.is_goal():
        return [state]
    else:
        # else, recurse on the possible next states
        result = []
        
        for s in state.next_states():
            # append all of the s
            result += dfs(s)
            
        return result
    
# uncomment this code when you're ready to test it out
#start_state = NQueenState(8)
#print(start_state)
#solutions = dfs(start_state)
#print("There were " + str(len(solutions)) + " solutions.\n")

#print(solutions[0])
