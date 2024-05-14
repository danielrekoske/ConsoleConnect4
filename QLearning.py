import numpy as np
import random
import pickle
from game_state import GameState

class QLearningBot:
    def __init__(self, token, alpha=0.1, gamma=0.9, epsilon=0.1, q_table=None):
        self.token = token
        self.alpha = alpha 
        self.gamma = gamma 
        self.epsilon = epsilon 
        self.q_table = q_table if q_table is not None else {}
        self.actions = list(range(GameState.COLUMNS))

    def get_state_key(self, state):
        return tuple(tuple(row) for row in state.board), state.current_player

    def get_q_value(self, state, action):
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(len(self.actions))
        return self.q_table[state_key][action]

    def update_q_value(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(len(self.actions))
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(len(self.actions))
        
        best_next_action = np.argmax(self.q_table[next_state_key])
        td_target = reward + self.gamma * self.q_table[next_state_key][best_next_action]
        self.q_table[state_key][action] += self.alpha * (td_target - self.q_table[state_key][action])

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(state.get_legal_moves())
        else:
            state_key = self.get_state_key(state)
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(len(self.actions))
            legal_moves = state.get_legal_moves()
            q_values = [self.q_table[state_key][a] for a in legal_moves]
            return legal_moves[np.argmax(q_values)]

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def get_move(self, game_state):
        return self.choose_action(game_state)
