import pygame
import sys
import numpy as np
import itertools

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
        board = [list(row) for row in state]
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    actions.append((i, j))
        return actions

    def perform_action(self, action, mark):
        row, col = action
        if self.board[row][col] is None:
            self.board[row][col] = mark
            if self.check_win():
                reward = 100
                self.done = True
            elif self.is_draw():
                reward = 10
                self.done = True
            else:
                reward = 0
            next_state = self.get_state()
            return next_state, reward
        return self.get_state(), 0

    def is_draw(self):
        for row in self.board:
            if None in row:
                return False
        return not self.check_win()

    def calculate_num_states(self):
        num_states = 0
        states = set()
        for board_state in itertools.product([None, 'X', 'O'], repeat=9):
            board = [board_state[i:i + 3] for i in range(0, 9, 3)]
            board_tuple = tuple(tuple(row) for row in board)
            if board_tuple not in states:
                num_states += 1
                states.add(board_tuple)
        return num_states

class ValueIteration:
    def __init__(self, env, discount_factor=1.0, theta=1e-9):
        self.env = env
        self.discount_factor = discount_factor
        self.theta = theta
        self.values = np.zeros(env.num_states)
        self.state_to_index_map = {state: idx for idx, state in enumerate(env.get_all_states())}

    def run(self):
        while True:
            delta = 0
            for state in self.env.get_all_states():
                idx = self.state_to_index_map[state]
                v = self.values[idx]
                new_value = self._calculate_new_value(state)
                self.values[idx] = new_value
                delta = max(delta, abs(v - new_value))
            if delta < self.theta:
                break
        return self.values

    def _calculate_new_value(self, state):
        new_value = 0
        for action in self.env.get_possible_actions(state):
            current_state = [row[:] for row in self.env.board]
            self.env.board = [list(row) for row in state]
            next_state, reward = self.env.perform_action(action, 'X')
            idx_next_state = self.state_to_index_map[next_state]
            new_value += reward + self.discount_factor * self.values[idx_next_state]
            self.env.board = current_state
        return new_value

    def make_move(self, env, mark):
        best_value = -np.inf
        best_action = None
        current_state = env.get_state()
        for action in env.get_possible_actions(current_state):
            original_state = [row[:] for row in env.board]
            env.board = [list(row) for row in current_state]
            next_state, _ = env.perform_action(action, mark)
            idx_next_state = self.state_to_index_map[next_state]
            if self.values[idx_next_state] > best_value:
                best_value = self.values[idx_next_state]
                best_action = action
            env.board = original_state
        if best_action:
            env.perform_action(best_action, mark)
            return best_action
        return None

def main():
    env = TicTacToeEnv()
    vi = ValueIteration(env)
    optimal_values = vi.run()

    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    print("Optimal State Values:")
    print(len(optimal_values))
    print(optimal_values)

    env.draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if env.handle_move(x, y, 'X'):
                    vi.make_move(env, 'O')
                    env.draw_board()
                    pygame.display.update()
        pygame.display.update()

if __name__ == "__main__":
    main()
