# environment.py
import pygame
import itertools
import sys

class TicTacToeEnv:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 300, 300
        self.LINE_WIDTH = 10
        self.BG_COLOR = (0, 0, 0)
        self.LINE_COLOR = (23, 145, 135)
        self.X_COLOR = (28, 170, 156)
        self.O_COLOR = (23, 145, 135)
        self.CELL_SIZE = self.WIDTH // 3
        self.CIRCLE_RADIUS = self.CELL_SIZE // 3
        self.CIRCLE_WIDTH = 15
        self.SPACE = self.CELL_SIZE // 4
        self.font = pygame.font.Font(None, 50)
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        
        self.board = [[None for _ in range(3)] for _ in range(3)]
        
        self.reset()
        self.num_states = self.calculate_num_states()

    def reset(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.done = False

    def draw_board(self):
        self.screen.fill(self.BG_COLOR)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, self.CELL_SIZE), (self.WIDTH, self.CELL_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, 2 * self.CELL_SIZE), (self.WIDTH, 2 * self.CELL_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.CELL_SIZE, 0), (self.CELL_SIZE, self.HEIGHT), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (2 * self.CELL_SIZE, 0), (2 * self.CELL_SIZE, self.HEIGHT), self.LINE_WIDTH)
        self.draw_marks()

    def draw_marks(self):
        for i in range(3):
            for j in range(3):
                mark = self.board[i][j]
                if mark == 'X':
                    pygame.draw.line(self.screen, self.X_COLOR, (j * self.CELL_SIZE + self.SPACE, i * self.CELL_SIZE + self.SPACE), 
                                     ((j + 1) * self.CELL_SIZE - self.SPACE, (i + 1) * self.CELL_SIZE - self.SPACE), self.LINE_WIDTH)
                    pygame.draw.line(self.screen, self.X_COLOR, ((j + 1) * self.CELL_SIZE - self.SPACE, i * self.CELL_SIZE + self.SPACE), 
                                     (j * self.CELL_SIZE + self.SPACE, (i + 1) * self.CELL_SIZE - self.SPACE), self.LINE_WIDTH)
                elif mark == 'O':
                    pygame.draw.circle(self.screen, self.O_COLOR, (j * self.CELL_SIZE + self.CELL_SIZE // 2, 
                                                                  i * self.CELL_SIZE + self.CELL_SIZE // 2), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)

    def check_win(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return True
        return False

    def handle_move(self, x, y, mark):
        row = y // self.CELL_SIZE
        col = x // self.CELL_SIZE
        if self.board[row][col] is None:
            self.board[row][col] = mark
            self.draw_board()
            pygame.display.update()
            if self.check_win():
                print(f"{mark} wins!")
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
            elif self.is_draw():
                print("It's a draw!")
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
            return True
        return False


    def get_state(self):
        return tuple(tuple(row) for row in self.board)

    def get_all_states(self):
        states = set()
        
        for board_state in itertools.product([None, 'X', 'O'], repeat=9):
            board = [board_state[i:i + 3] for i in range(0, 9, 3)]
            board_tuple = tuple(tuple(row) for row in board)
            states.add(board_tuple)
        
        return states
    def get_possible_actions(self, state):
        actions = []
        # Convert state from tuple of tuples to a list of lists for easier manipulation
        board = [list(row) for row in state]
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    actions.append((i, j))
        return actions
    # def get_possible_actions(self):
    #     actions = []
    #     for i in range(3):
    #         for j in range(3):
    #             if self.board[i][j] is None:
    #                 actions.append((i, j))
    #     return actions

    def perform_action(self, action, mark):
        row, col = action
        if self.board[row][col] is None:
            self.board[row][col] = mark
            if self.check_win():
                reward = 10
                self.done = True
            elif self.is_draw():
                reward = 5
                self.done = True
            else:
                reward = 0   # Neutral reward for valid moves
            next_state = self.get_state()
            return next_state, reward
        else:
        # If the move is invalid, do not change the board and return the same state with zero reward
            return self.get_state(), 1
    def is_draw(self):
        for row in self.board:
            if None in row:
                return False
        return not self.check_win()

    def is_done(self):
        return self.done
    def calculate_num_states(self):
        num_states = 0
        states = set()
    
        for board_state in itertools.product([None, 'X', 'O'], repeat=9):
        # Convert the board_state into a tuple of tuples for immutability and hashing
            board = [board_state[i:i + 3] for i in range(0, 9, 3)]
            board_tuple = tuple(tuple(row) for row in board)
        
            if board_tuple not in states:
                num_states += 1
                states.add(board_tuple)
    
        return num_states
    
    # def calculate_num_states(self):
    #     num_states = 0
    #     states = set()
        
    #     for board_state in itertools.product([None, 'X', 'O'], repeat=9):
    #         board = [list(board_state[i:i + 3]) for i in range(0, 9, 3)]
    #         if board not in states:
    #             num_states += 1
    #             states.add(tuple(map(tuple, board)))
                
    #     return num_states
    
'''Explanation of New Methods:
get_state():

Returns the current board state as a tuple of tuples, which is useful for representing states in a format suitable for Value Iteration.
get_possible_actions():

Returns a list of possible actions (empty cells) that can be performed. This helps in determining the valid actions for the agent.
perform_action(action, mark):

Applies the action to the board and returns the new state and reward. The reward can be adjusted based on game rules (e.g., 1 for a win, 0 for a regular move, -1 for invalid actions).
is_done():

Indicates if the game is over. This helps to check the termination condition in Value Iteration.'''
