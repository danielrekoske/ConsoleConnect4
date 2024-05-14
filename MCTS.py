import random
import math
from game_state import GameState
class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.move = move

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def most_visited_child(self):
        return max(self.children, key=lambda child: child.visits)

class MCTS:
    def __init__(self, num_simulations):
        self.num_simulations = num_simulations

    def search(self, initial_state):
        root = Node(initial_state)
        
        for _ in range(self.num_simulations):
            node = self._tree_policy(root)
            reward = self._default_policy(node.state)
            self._backup(node, reward)
        
        return root.most_visited_child().move

    def _tree_policy(self, node):
        while not node.state.is_game_over():
            if not node.is_fully_expanded():
                return self._expand(node)
            else:
                node = node.best_child()
        return node

    def _expand(self, node):
        legal_moves = node.state.get_legal_moves()
        tried_moves = [child.move for child in node.children]
        for move in legal_moves:
            if move not in tried_moves:
                new_state = node.state.clone()
                new_state.make_move(move)
                new_node = Node(new_state, parent=node, move=move)
                node.children.append(new_node)
                return new_node
        raise Exception("Shouldn't reach here: No untried moves")

    def _default_policy(self, state):
        current_state = state.clone()
        while not current_state.is_game_over():
            move = random.choice(current_state.get_legal_moves())
            current_state.make_move(move)
        if current_state.winning_move('X'):
            return 1
        elif current_state.winning_move('O'):
            return -1
        else:
            return 0

    def _backup(self, node, reward):
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent
