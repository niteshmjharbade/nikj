# environment.py
import pygame
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
            return True
        return False
