import numpy as np
from utils.env import TicTacToeEnv  # Adjust import based on your structure


class ValueIteration:
    def __init__(self, env, discount_factor=1.0, theta=1e-6):
        self.env = env
        self.discount_factor = discount_factor
        self.theta = theta  # Convergence threshold
        self.values = np.zeros(env.num_states)  # Initialize state values
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
        result = self.values.tolist() if hasattr(self.values, 'tolist') else list(self.values)
        return result

    def _calculate_new_value(self, state):
        new_value = 0
        for action in self.env.get_possible_actions(state):
            # Save current state
            current_state = [row[:] for row in self.env.board]
            self.env.board = [list(row) for row in state]  # Set the board to the current state
            next_state, reward = self.env.perform_action(action, 'X')
            idx_next_state = self.state_to_index_map[next_state]
            new_value += reward + self.discount_factor * self.values[idx_next_state]
            # Restore original state
            self.env.board = current_state
        return new_value

    def make_move(self, env, mark):
        best_value = -np.inf
        best_action = None
        current_state = env.get_state()
        for action in env.get_possible_actions(current_state):
            # Save current state
            original_state = [row[:] for row in env.board]
            env.board = [list(row) for row in current_state]  # Set the board to the current state
            next_state, _ = env.perform_action(action, mark)
            idx_next_state = self.state_to_index_map[next_state]
            if self.values[idx_next_state] > best_value:
                best_value = self.values[idx_next_state]
                best_action = action
            # Restore original state
            env.board = original_state
        if best_action:
            env.perform_action(best_action, mark)
            return best_action
        return None
# import numpy as np
# from utils.env import TicTacToeEnv  # Adjust import based on your structure

# class ValueIteration:
#     def __init__(self, env, discount_factor=1.0, theta=1e-6):
#         self.env = env
#         self.discount_factor = discount_factor
#         self.theta = theta  # Convergence threshold
#         self.values = np.zeros(env.num_states)  # Initialize state values
#         self.state_to_index_map = {state: idx for idx, state in enumerate(env.get_all_states())}

#     def run(self):
#         while True:
#             delta = 0
#             for state in self.env.get_all_states():
#                 idx = self.state_to_index_map[state]
#                 v = self.values[idx]
#                 new_value = self._calculate_new_value(state)
#                 self.values[idx] = new_value
#                 delta = max(delta, abs(v - new_value))
#             if delta < self.theta:
#                 break
#         return self.values

#     def _calculate_new_value(self, state):
#         new_value = 0
#         for action in self.env.get_possible_actions(state):
#             next_state, reward = self.env.perform_action(action, 'X')
#             idx_next_state = self.state_to_index_map[next_state]
#             new_value += reward + self.discount_factor * self.values[idx_next_state]
#         return new_value

#     def make_move(self, env, mark):
#         best_value = -np.inf
#         best_action = None
#         current_state = env.get_state()
#         for action in env.get_possible_actions(current_state):
#             next_state, _ = env.perform_action(action, mark)
#             idx_next_state = self.state_to_index_map[next_state]
#             if self.values[idx_next_state] > best_value:
#                 best_value = self.values[idx_next_state]
#                 best_action = action
#         if best_action:
#             env.perform_action(best_action, mark)
#             return best_action
#         return None
# # import numpy as np
# # from utils.env import TicTacToeEnv  # Adjust import based on your structure

# # class ValueIteration:
# #     def __init__(self, env, discount_factor=1.0, gamma=1e-6, theta=1e-6):
# #         self.env = env
# #         self.discount_factor = discount_factor
# #         self.gamma = gamma
# #         self.theta = theta  # Add theta for convergence threshold
# #         self.values = np.zeros(self.env.num_states)  # Initialize state values
# #         self.state_to_index_map = {state: idx for idx, state in enumerate(env.get_all_states())}

# #     def run(self):
# #         while True:
# #             delta = 0
# #             for state in self.env.get_all_states():
# #                 idx = self.state_to_index_map[state]
# #                 v = self.values[idx]
# #                 new_value = self._calculate_new_value(state)
# #                 self.values[idx] = new_value  # Use idx for indexing
# #                 delta = max(delta, abs(v - new_value))
# #             if delta < self.theta:
# #                 break
# #         return self.values

# #     def _calculate_new_value(self, state):
# #         new_value = 0
# #         for action in self.env.get_possible_actions(state):
# #             next_state, reward = self.env.perform_action(action, mark='X')
# #             idx_next_state = self.state_to_index_map[next_state]
# #             new_value += reward + self.gamma * self.values[idx_next_state]
# #         return new_value
# # # import numpy as np
# # # from utils.env import TicTacToeEnv  # Adjust import based on your structure

# # # class ValueIteration:
# # #     def __init__(self, env, discount_factor=1.0, gamma=1e-6, theta=1e-6):
# # #         self.env = env
# # #         self.discount_factor = discount_factor
# # #         self.gamma = gamma
# # #         self.theta = theta  # Add theta for convergence threshold
# # #         self.values = np.zeros(self.env.num_states)  # Initialize state values
# # #         self.state_to_index_map = {state: idx for idx, state in enumerate(env.get_all_states())}

# # #     def run(self):
# # #         while True:
# # #             delta = 0
# # #             for state in self.env.get_all_states():
# # #                 idx = self.state_to_index_map[state]
# # #                 v = self.values[idx]
# # #                 new_value = self._calculate_new_value(state)
# # #                 self.values[idx] = new_value  # Use idx for indexing
# # #                 delta = max(delta, abs(v - new_value))
# # #             if delta < self.theta:
# # #                 break
# # #         return self.values

# # #     def _calculate_new_value(self, state):
# # #         new_value = 0
# # #         for action in self.env.get_possible_actions(state):
# # #             next_state, reward = self.env.perform_action(action, mark='X')
# # #             idx_next_state = self.state_to_index_map[next_state]
# # #             new_value += reward + self.gamma * self.values[idx_next_state]
# # #         return new_value

# # # # Example usage
# # # if __name__ == "__main__":
# # #     env = TicTacToeEnv()  # Create environment
# # #     vi = ValueIteration(env)
# # #     optimal_values = vi.run()
# # #     print("Optimal State Values:")
# # #     print(optimal_values)
