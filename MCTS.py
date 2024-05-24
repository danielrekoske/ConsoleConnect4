import random
import math
import copy

class MCTS:
    def __init__(self, exploration_weight=1):
        self.exploration_weight = exploration_weight

    def select(self, node):
        best_value = float("-inf")
        best_nodes = []
        for child in node.children:
            uct_value = (child.wins / child.visits) + self.exploration_weight * math.sqrt(
                math.log(node.visits) / child.visits
            )
            if uct_value > best_value:
                best_value = uct_value
                best_nodes = [child]
            elif uct_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def expand(self, node, game):
        if node.is_terminal:
            return
        for move in game.get_legal_moves():
            child = Node(parent=node, move=move, game=copy.deepcopy(game))
            node.children.append(child)

    def simulate(self, node):
        game = copy.deepcopy(node.game)
        while not game.is_terminal():
            move = random.choice(game.get_legal_moves())
            game.apply_move(move)
        return game.get_winner()

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            if result == node.game.current_player:
                node.wins += 1
            node = node.parent

    def get_best_move(self, root, game, heuristic_func):
        self.expand(root, game)
        
        heuristic_scores = [(child, heuristic_func(child.game)) for child in root.children]
        heuristic_scores.sort(key=lambda x: x[1], reverse=True)
        top_nodes = [x[0] for x in heuristic_scores[:3]] 

        for i in range(1000): 
            for node in top_nodes:
                leaf = self.select(node)
                self.expand(leaf, game)
                result = self.simulate(leaf)
                self.backpropagate(leaf, result)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

class Node:
    def __init__(self, parent=None, move=None, game=None):
        self.parent = parent
        self.move = move
        self.game = game
        self.wins = 0
        self.visits = 0
        self.children = []
        self.is_terminal = game.is_game_over() if game else False
