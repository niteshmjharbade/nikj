import random
#from nim import Nim

class NimValueIteration:
    def __init__(self, gamma=0.9, theta=0.0001):
        self.gamma = gamma  # Discount factor
        self.theta = theta  # Convergence threshold
        self.values = {}    # State values

    def value_iteration(self, nim):
        # Initialize value function
        for state in self.all_states(nim):
            self.values[state] = 0 if self.is_terminal(state) else random.random()

        while True:
            delta = 0
            for state in self.all_states(nim):
                if self.is_terminal(state):
                    continue
                v = self.values[state]
                self.values[state] = self.best_value(state)
                delta = max(delta, abs(v - self.values[state]))
            if delta < self.theta:
                break

    def best_value(self, state):
        return max(self.state_value(state, action) 
                   for action in Nim.available_actions(state))

    def state_value(self, state, action):
        next_state = self.get_next_state(state, action)
        return self.get_reward(state, action) + self.gamma * self.values[next_state]

    def get_policy(self):
        policy = {}
        for state in self.values:
            if not self.is_terminal(state):
                policy[state] = max(Nim.available_actions(state),
                                    key=lambda a: self.state_value(state, a))
        return policy

    def all_states(self, nim):
        def generate_states(current_state, max_piles):
            if len(current_state) == len(max_piles):
                yield tuple(current_state)
                return
            for i in range(max_piles[len(current_state)] + 1):
                yield from generate_states(current_state + [i], max_piles)

        return list(generate_states([], nim.piles))

    def is_terminal(self, state):
        return all(pile == 0 for pile in state)

    def get_next_state(self, state, action):
        new_state = list(state)
        pile, count = action
        new_state[pile] -= count
        return tuple(new_state)

    def get_reward(self, state, action):
        next_state = self.get_next_state(state, action)
        if self.is_terminal(next_state):
            return -1  # The player who makes the last move loses
        return 0

    def choose_action(self, state):
        return max(Nim.available_actions(state),
                   key=lambda a: self.state_value(state, a))