# agent.py
import random

class RandomAgent:
    def __init__(self):
        pass

    def make_move(self, board, mark):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = mark
