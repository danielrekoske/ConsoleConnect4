import random
import pickle
from Player import Player
from game_state import GameState, EMPTY_SLOT
from MCTS import MCTS

class BotPlayer(Player):
    def __init__(self, token, difficulty):
        super().__init__(token)
        self.difficulty = difficulty
        self.opponent_token = 'X' if token == 'O' else 'O'
        self.q_table = None

    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

    def get_move(self, game_state):
        move_func = getattr(self, f"move_{self.difficulty}", None)
        if move_func:
            return move_func(game_state)
        return self.move_0(game_state)

    def move_0(self, state):
        valid_columns = [col for col in range(GameState.COLUMNS) if state.board[0][col] == EMPTY_SLOT]
        return random.choice(valid_columns) if valid_columns else None

    def move_1(self, state):
        for col in range(GameState.COLUMNS):
            if self.is_winning_move(state.board, col, self.token):
                return col
        return self.move_0(state.board)

    def move_2(self, state):
        for col in range(GameState.COLUMNS):
            if self.is_winning_move(state.board, col, self.opponent_token):
                return col
        return self.move_1(state.board)
    
    def move_3(self, state):
        return self.minimax_search(state.board, self.difficulty, float('-inf'), float('inf'), True)[1]
    
    def move_4(self, state):
        return self.minimax_search(state.board, self.difficulty, float('-inf'), float('inf'), True)[1]

    def move_5(self, state):
        return self.minimax_search(state.board, self.difficulty, float('-inf'), float('inf'), True)[1]
    
    def move_6(self, state):
        mcts = MCTS(num_simulations = 1000)
        return mcts.search(state)

    def move_7(self, state):
        return self.q_learning_move(state)
    
    def minimax_search(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over(board):
            return self.evaluate(board, self.token), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for col in range(GameState.COLUMNS):
                if self.is_valid_location(board, col):
                    temp_board = self.get_temp_board(board, col, self.token)
                    eval_val, _ = self.minimax_search(temp_board, depth - 1, alpha, beta, False)
                    if eval_val > max_eval:
                        max_eval = eval_val
                        best_move = col
                    alpha = max(alpha, eval_val)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for col in range(GameState.COLUMNS):
                if self.is_valid_location(board, col):
                    temp_board = self.get_temp_board(board, col, self.opponent_token)
                    eval_val, _ = self.minimax_search(temp_board, depth - 1, alpha, beta, True)
                    if eval_val < min_eval:
                        min_eval = eval_val
                        best_move = col
                    beta = min(beta, eval_val)
                    if beta <= alpha:
                        break 
            return min_eval, best_move
    
    def is_winning_move(self, board, col, token):
        temp_board = [row[:] for row in board]
        self.drop_piece(temp_board, col, token)
        return self.winning_move(temp_board, token)

    def drop_piece(self, board, col, token):
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] == EMPTY_SLOT:
                board[row][col] = token
                return

    def winning_move(self, board, token):
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                if board[row][col] == token and \
                   board[row][col+1] == token and \
                   board[row][col+2] == token and \
                   board[row][col+3] == token:
                    return True

        for row in range(len(board) - 3):
            for col in range(len(board[0])):
                if board[row][col] == token and \
                   board[row+1][col] == token and \
                   board[row+2][col] == token and \
                   board[row+3][col] == token:
                    return True

        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] == token and \
                   board[row+1][col+1] == token and \
                   board[row+2][col+2] == token and \
                   board[row+3][col+3] == token:
                    return True

        for row in range(3, len(board)):
            for col in range(len(board[0]) - 3):
                if board[row][col] == token and \
                   board[row-1][col+1] == token and \
                   board[row-2][col+2] == token and \
                   board[row-3][col+3] == token:
                    return True

        return False
    
    def evaluate(self, board, token):
        opponent_token = 'X' if token == 'O' else 'O'
        score = 0

        for row in board:
            score += self.evaluate_sequence(row, token)

        for col in range(len(board[0])):
            column = [board[row][col] for row in range(len(board))]
            score += self.evaluate_sequence(column, token)

        for i in range(len(board) - 3):
            for j in range(len(board[0]) - 3):
                diagonal = [board[i + k][j + k] for k in range(4)]
                score += self.evaluate_sequence(diagonal, token)

        for i in range(3, len(board)):
            for j in range(len(board[0]) - 3):
                diagonal = [board[i - k][j + k] for k in range(4)]
                score += self.evaluate_sequence(diagonal, token)

        score += 1000 * (self.check_winning_move(board, token) - self.check_winning_move(board, opponent_token))

        center_column = [board[row][len(board[0]) // 2] for row in range(len(board))]
        score += self.evaluate_sequence(center_column, token)

        return score
    
    def evaluate_sequence(self, sequence, token):
        score = 0
        for i in range(len(sequence) - 3):
            window = sequence[i:i+4]
            if window.count(token) == 4:
                score += 10000
            elif window.count(token) == 3 and window.count(EMPTY_SLOT) == 1:
                score += 100
            elif window.count(token) == 2 and window.count(EMPTY_SLOT) == 2:
                score += 10
            elif window.count(token) == 1 and window.count(EMPTY_SLOT) == 3:
                score += 1
        return score
    
    def check_winning_move(self, board, token):
        count = 0
        for col in range(len(board[0])):
            if self.is_valid_location(board, col):
                temp_board = self.get_temp_board(board, col, token)
                if self.winning_move(temp_board, token):
                    count += 1
        return count
    
    def game_over(self, board):
        return self.winning_move(board, self.token) or self.winning_move(board, self.opponent_token) or self.is_board_full(board)

    def is_valid_location(self, board, col):
        return board[0][col] == EMPTY_SLOT

    def get_temp_board(self, board, col, token):
        temp_board = [row[:] for row in board]
        for row in range(GameState.ROWS - 1, -1, -1):
            if temp_board[row][col] == EMPTY_SLOT:
                temp_board[row][col] = token
                break
        return temp_board

    def is_board_full(self, board):
        for col in range(GameState.COLUMNS):
            if self.is_valid_location(board, col):
                return False
        return True

    def q_learning_move(self, state):
        if self.q_table is None:
            self.load_q_table('q_table.pkl')

        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            return self.move_0(state)

        q_values = self.q_table[state_key]
        legal_moves = state.get_legal_moves()
        max_q_value = float('-inf')
        best_move = None

        for move in legal_moves:
            if q_values[move] > max_q_value:
                max_q_value = q_values[move]
                best_move = move

        return best_move if best_move is not None else self.move_0(state)

    def get_state_key(self, state):
        return tuple(tuple(row) for row in state.board), state.current_player
