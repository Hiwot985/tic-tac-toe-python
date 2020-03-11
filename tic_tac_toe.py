
import random
from math import inf


class TicTacToe:
    def __init__(self, user_choice, ai_choice, user_first_player):
        """
        Constructor
        :param user_choice: Either X or O
        :param ai_choice: Either X or O but not same as user_choice
        :param user_first_player: Either Y or N
        """
        self.board = self.get_board()  # For getting the default board state
        self.user_choice = user_choice
        self.ai_choice = ai_choice
        self.user_first_player = user_first_player
        self.user_val = -1  # Not a real score but just to mark -1 on the board for the user
        self.ai_val = 1  # Not a real score but just to make 1 on the board for the AI

    @staticmethod
    def get_board():
        """
        Responsible for initializing the empty board,
        which is essentially an array of array of dimension 3 X 3
        :return: Initial board state initialized with 0
        """
        return [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def draw_board(self):
        """
        For drawing the board in the terminal
        :return: void
        """
        points = {
            -1: self.user_choice,
            +1: self.ai_choice,
            0: ' '
        }
        for row in self.board:
            print('\n' + '----------------')
            for item in row:
                print(f'| {points[item]} |', end='')
        print('\n' + '----------------')

    def calculate_state(self):
        """
        Calculates board state which is essentially 0 values and
        returns in the form of [X, Y],
        where X is the row number and Y is the column number
        :return: List of list of X and Y. e.g [[1, 2], [2, 0]]
        """
        empty_cells = []
        for x, row in enumerate(self.board):
            # Iterating for each row
            for y, item in enumerate(row):
                # Iterating for each item in the row
                if item == 0:
                    empty_cells.append([x, y])

        return empty_cells

    @staticmethod
    def get_cell_no_from_move(move_no):
        """
        Converts numerical move number (between 1 -9) to valid board co-ordinate in [X, Y] format
        :param move_no: 1 - 9
        :return: [X, Y] where X is row and Y is column number
        """
        row = (move_no - 1) // 3
        col = (move_no - 1) % 3
        return [row, col]

    def perform_move(self, cell, player_value):
        """
        Performs move and overwrites the current state
        :param cell: Cell is a list containing X and Y co ordinates
        :param player_value: player value is -1 if User and 1 if AI
        :return: Boolean depending on the move if its valid
        """
        if cell in self.calculate_state():
            self.board[cell[0]][cell[1]] = player_value
            return True
        else:
            return False

    def user_turn(self):
        """
        User turn to play a valid move
        :return: void
        """
        print(f'User turn [{self.user_choice}]')
        self.draw_board()
        move = -1
        while move < 1 or move > 9:
            move = int(input('Please enter a move between 1 - 9: '))
            cell = self.get_cell_no_from_move(move)
            valid_move = self.perform_move(cell, self.user_val)
            if not valid_move:
                print('Please enter a valid move !!!!')
                move = -1

    def win_moves(self, player):
        """
        Generates a list of all the win moves and their states respectively.
        Checks if the player matches with any of the win states
        :param player: Player can be AI or the user
        :return: Boolean depending on the winning state of the player
        """
        # Stores all the states
        states = []

        # Below is the function to generate all the winning moves
        diag_1 = []
        diag_2 = []

        for i in range(3):
            row_temp_state = []
            col_temp_state = []

            # To Compute the left diagonal ( \ ) state
            diag_1.append(self.board[i][i])
            # To computer the other diagonal ( / )
            diag_2.append(self.board[2 - i][i])

            for j in range(3):
                # Compute the horizontal row win
                row_temp_state.append(self.board[i][j])
                # Compute the vertical col win
                col_temp_state.append(self.board[j][i])

            # Append everything to the state declared above
            states.append(row_temp_state)
            states.append(col_temp_state)

        states.append(diag_1)
        states.append(diag_2)

        # Check if the player is won or not and return appropriately
        if [player, player, player] in states:
            return True
        else:
            return False

    def get_score(self):
        """
        Computes score based who won the game
        :return: score (int)
        """
        if self.win_moves(self.user_val):
            score = -1
        elif self.win_moves(self.ai_val):
            score = 1
        else:
            score = 0

        return score

    def determine_end(self):
        """
        Checks if anyone won the game or not
        :return: Boolean True if anyone won else False
        """
        return self.win_moves(self.ai_val) or self.win_moves(self.user_val)

    def min_max_algorithm(self, player):
        """
        The AI Brain behind tic tac toe game. Mostly used in 2 player games like chess, tic-tac-toe, etc.
        The algorithm searches recursively for the best available move, so that it leads to win or not lose (draw).

        It iterates over the current board state and keeps playing until it reaches a terminal state
        where it cannot move and then records the score. This iteration is done for every empty cell on the board.

        :param player: User or AI
        :return: Score of the format [x, y, score]
        where x,y are the board co-ordinates and score is the score obtained.
        """
        if player == self.ai_val:
            best_score = [-1, -1, -inf]
        else:
            best_score = [-1, -1, inf]
        remaining_empty_cells = self.calculate_state()

        if len(remaining_empty_cells) == 0 or self.determine_end():
            final_score = self.get_score()
            return [-1, -1, final_score]

        for item in remaining_empty_cells:
            x, y = item[0], item[1]
            self.board[x][y] = player
            final_score = self.min_max_algorithm(-player)
            self.board[x][y] = 0
            final_score[0], final_score[1] = x, y

            if player == self.ai_val:
                if final_score[2] > best_score[2]:
                    best_score = final_score
            else:
                if final_score[2] < best_score[2]:
                    best_score = final_score

        return best_score

    def ai_turn(self):
        """
        AI turn to play a valid move.
        It call the above minmax algorithm.
        If playing first, it randomly selects X,Y co-ordinates for the board
        :return: void
        """
        print(f'AI turn [{self.ai_choice}]')
        self.draw_board()

        # If AI is the first player and the board is untouched then choose a random cell
        if len(self.calculate_state()) == 9:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        else:
            # Call the min max algorithm
            ai_move = self.min_max_algorithm(self.ai_val)
            x, y = ai_move[0], ai_move[1]

        self.perform_move([x, y], self.ai_val)

    def main(self):
        """
        Main function to run tic-tac-tow game.
        :return:
        """

        # Keep playing until all the moves are exhausted or if someone is won
        while len(self.calculate_state()) > 0 and not self.determine_end():
            if self.user_first_player.casefold() == 'N'.casefold():
                self.ai_turn()
                self.user_first_player = ''
            self.user_turn()
            self.ai_turn()

        # Plot the Board & end message
        if self.win_moves(self.user_val):
            print('\n')
            self.draw_board()
            print('You just defeated AI !!!')
        elif self.win_moves(self.ai_val):
            print('\n')
            self.draw_board()
            print('You SIR, lost to a computer !!!')
        else:
            print('\n')
            self.draw_board()
            print('You are TOUGH.. Call it a DRAW !!!')


if __name__ == "__main__":

    u_first_player = ''
    u_choice = ''
    a_i_choice = ''

    # Take the user's input of playing X or O
    while u_choice.casefold() != 'X'.casefold() and u_choice.casefold() != 'O'.casefold():
        u_choice = input('Would you like to play X or O: ').upper()
        a_i_choice = 'O' if u_choice.casefold() == 'X'.casefold() else 'X'

    # Who wants to start first ?
    while u_first_player.casefold() != 'Y'.casefold() and u_first_player.casefold() != 'N'.casefold():
        u_first_player = input('Would you like to play first? Y / N: ')

    # Create an object of the above class and then call the main function
    t = TicTacToe(u_choice, a_i_choice, u_first_player)
    t.main()
