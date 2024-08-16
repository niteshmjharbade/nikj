import random
# from nim import Nim
class NimPolicyIteration:
    def __init__(self, gamma=0.9):
        self.gamma = gamma
        self.values = {}
        self.policy = {}

    def policy_iteration(self, nim):
        # Initialize random policy
        for state in self.all_states(nim):
            self.policy[state] = random.choice(list(Nim.available_actions(state)))

        while True:
            # Policy Evaluation
            self.policy_evaluation()

            # Policy Improvement
            policy_stable = True
            for state in self.all_states(nim):
                if self.is_terminal(state):
                    continue
                old_action = self.policy[state]
                self.policy[state] = max(Nim.available_actions(state),
                                         key=lambda a: self.q_value(state, a))
                if old_action != self.policy[state]:
                    policy_stable = False

            if policy_stable:
                break

    def policy_evaluation(self):
        while True:
            delta = 0
            for state in self.all_states(nim):
                if self.is_terminal(state):
                    continue
                v = self.values.get(state, 0)
                self.values[state] = self.q_value(state, self.policy[state])
                delta = max(delta, abs(v - self.values[state]))
            if delta < self.theta:
                break

    def q_value(self, state, action):
        next_state = self.get_next_state(state, action)
        return self.get_reward(state, action) + self.gamma * self.values.get(next_state, 0)

    # Helper methods (same as in ValueIteration)
    # ...