import numpy as np
import pygame
import sys
from utils.env import TicTacToeEnv
from utils.agent import RandomAgent
from ai_bot.value_iteration import ValueIteration

def main():
    # Initialize environment and agents
    env = TicTacToeEnv()
    agent = RandomAgent()
    vi = ValueIteration(env)  # Create instance of Value Iteration
    
    # Run Value Iteration to get optimal state values and policy
    optimal_values = vi.run()
    
    # Set NumPy print options to display the full array
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    
    print("Optimal State Values:")
    print(len(optimal_values))
   # print(optimal_values.shape)
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
                    agent.make_move(env.board, 'O')  # Make a move using RandomAgent
                    env.draw_board()
                    pygame.display.update()
        pygame.display.update()

if __name__ == "__main__":
    
    main()
# import pygame
# import sys
# from utils.env import TicTacToeEnv
# from ai_bot.value_iteration import ValueIteration

# def main():
#     # Initialize environment and value iteration
#     env = TicTacToeEnv()
#     vi = ValueIteration(env)
    
#     # Run Value Iteration to get optimal state values
#     optimal_values = vi.run()
#     print("Optimal State Values:")
#     print(optimal_values)
    
#     # Initialize pygame
#     pygame.init()
#     screen = pygame.display.set_mode((300, 300))
#     pygame.display.set_caption("Tic-Tac-Toe")
#     env.draw_board()
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 x, y = pygame.mouse.get_pos()
#                 if env.handle_move(x, y, 'X'):
#                     if env.check_win() or env.is_done():
#                         pygame.quit()
#                         sys.exit()
#                     vi.make_move(env, 'O')  # Make a move using ValueIteration results
#                     if env.check_win() or env.is_done():
#                         pygame.quit()
#                         sys.exit()
#                     env.draw_board()
#                     pygame.display.update()
#         pygame.display.update()

# if __name__ == "__main__":
#     main()
# # import pygame
# # import sys
# # from utils.env import TicTacToeEnv
# # from ai_bot.value_iteration import ValueIteration

# # def main():
# #     # Initialize environment and value iteration
# #     env = TicTacToeEnv()
# #     vi = ValueIteration(env)
    
# #     # Run Value Iteration to get optimal state values
# #     optimal_values = vi.run()
# #     print("Optimal State Values:")
# #     print(optimal_values)
    
# #     # Initialize pygame
# #     pygame.init()
# #     screen = pygame.display.set_mode((300, 300))
# #     pygame.display.set_caption("Tic-Tac-Toe")
# #     env.draw_board()
    
# #     while True:
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 pygame.quit()
# #                 sys.exit()
# #             if event.type == pygame.MOUSEBUTTONDOWN:
# #                 x, y = pygame.mouse.get_pos()
# #                 if env.handle_move(x, y, 'X'):
# #                     if env.check_win() or env.is_done():
# #                         pygame.quit()
# #                         sys.exit()
# #                     vi.make_move(env, 'O')  # Make a move using ValueIteration results
# #                     if env.check_win() or env.is_done():
# #                         pygame.quit()
# #                         sys.exit()
# #                     env.draw_board()
# #                     pygame.display.update()
# #         pygame.display.update()

# # if __name__ == "__main__":
# #     main()
# # # import pygame

# # # import sys
# # # from utils.env import TicTacToeEnv
# # # from ai_bot.value_iteration import ValueIteration

# # # def main():
# # #     # Initialize environment and value iteration
# # #     env = TicTacToeEnv()
# # #     vi = ValueIteration(env)
    
# # #     # Run Value Iteration to get optimal state values
# # #     optimal_values = vi.run()
# # #     print("Optimal State Values:")
# # #     print(optimal_values)
    
# # #     # Initialize pygame
# # #     pygame.init()
# # #     screen = pygame.display.set_mode((300, 300))
# # #     pygame.display.set_caption("Tic-Tac-Toe")
# # #     env.draw_board()
    
# # #     while True:
# # #         for event in pygame.event.get():
# # #             if event.type == pygame.QUIT:
# # #                 pygame.quit()
# # #                 sys.exit()
# # #             if event.type == pygame.MOUSEBUTTONDOWN:
# # #                 x, y = pygame.mouse.get_pos()
# # #                 if env.handle_move(x, y, 'X'):
# # #                     if env.check_win() or env.is_draw():
# # #                         pygame.quit()
# # #                         sys.exit()
# # #                     vi.make_move(env, 'O')  # Make a move using ValueIteration results
# # #                     if env.check_win() or env.is_draw():
# # #                         pygame.quit()
# # #                         sys.exit()
# # #                     env.draw_board()
# # #                     pygame.display.update()
# # #         pygame.display.update()

# # # if __name__ == "__main__":
# # #     main()
# # # # import pygame
# # # # import sys
# # # # from utils.env import TicTacToeEnv
# # # # from utils.agent import RandomAgent
# # # # from ai_bot.value_iteration import ValueIteration

# # # # def main():
# # # #     # Initialize environment and agents
# # # #     env = TicTacToeEnv()
# # # #     agent = RandomAgent()
# # # #     vi = ValueIteration(env)  # Create instance of Value Iteration
    
# # # #     # Run Value Iteration to get optimal state values and policy
# # # #     optimal_values = vi.run()
# # # #     print("Optimal State Values:")
# # # #     print(optimal_values)
    
# # # #     env.draw_board()
# # # #     while True:
# # # #         for event in pygame.event.get():
# # # #             if event.type == pygame.QUIT:
# # # #                 pygame.quit()
# # # #                 sys.exit()
# # # #             if event.type == pygame.MOUSEBUTTONDOWN:
# # # #                 x, y = pygame.mouse.get_pos()
# # # #                 if env.handle_move(x, y, 'X'):
# # # #                     agent.make_move(env.board, 'O')  # Make a move using RandomAgent
# # # #                     env.draw_board()
# # # #                     pygame.display.update()
# # # #         pygame.display.update()

# # # # if __name__ == "__main__":
# # # #     main()
