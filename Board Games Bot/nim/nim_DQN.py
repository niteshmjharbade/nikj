import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
    
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, available_actions):
        if np.random.rand() <= self.epsilon:
            return random.randrange(len(available_actions))
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        act_values = self.model(state)
        action_index = np.argmax(act_values.cpu().data.numpy())
        if action_index >= len(available_actions):
            action_index = random.randrange(len(available_actions))
        return action_index

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
                target = (reward + self.gamma *
                          np.amax(self.model(next_state).cpu().data.numpy()))
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            target_f = self.model(state)
            target_f[0][action] = target
            loss = nn.MSELoss()(self.model(state), target_f)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
class Nim:
    def __init__(self, initial=[1, 3, 5, 7]):
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    def available_actions(self):
        actions = []
        for i, pile in enumerate(self.piles):
            for j in range(1, pile + 1):
                actions.append((i, j))
        return actions

    def make_move(self, action):
        pile, count = action
        self.piles[pile] -= count
        self.player = 1 - self.player
        if all(pile == 0 for pile in self.piles):
            self.winner = 1 - self.player
        return self.get_state(), self.winner is not None

    def get_state(self):
        return self.piles.copy()
    
def train_dqn(episodes):
    state_size = 4  # Assuming 4 piles in Nim
    action_size = len(Nim().available_actions())
    agent = DQNAgent(state_size, action_size)
    batch_size = 32

    for e in range(episodes):
        game = Nim()
        state = game.get_state()
        for time in range(500):  # Max 500 moves per game
            available_actions = game.available_actions()
            action_index = agent.act(state, available_actions)
            action = available_actions[action_index]
            next_state, done = game.make_move(action)
            reward = -1 if done else 0
            agent.remember(state, action_index, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e}/{episodes}, score: {time}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

    return agent

def play_against_dqn(agent):
    game = Nim()
    state = game.get_state()
    while True:
        print(f"Current state: {state}")
        if game.player == 0:
            available_actions = game.available_actions()
            action_index = agent.act(state, available_actions)
            action = available_actions[action_index]
        else:
            available_actions = game.available_actions()
            print("Available actions:", available_actions)
            pile = int(input("Choose pile: "))
            count = int(input("Choose count: "))
            action = (pile, count)
        next_state, done = game.make_move(action)
        print(f"Player {1 - game.player} took {action[1]} from pile {action[0]}")
        state = next_state
        if done:
            print(f"Player {game.winner} lost!")
            break

# Train the agent
trained_agent = train_dqn(5000)

# Play against the trained agent
play_against_dqn(trained_agent)
