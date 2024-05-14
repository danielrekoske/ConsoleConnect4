EMPTY_SLOT = ' '

class GameState:
    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.board = [[EMPTY_SLOT] * self.COLUMNS for _ in range(self.ROWS)]
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('+---+---+---+---+---+---+---+')
        print('| 1 | 2 | 3 | 4 | 5 | 6 | 7 |')
        print('+---+---+---+---+---+---+---+')

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY_SLOT

    def get_legal_moves(self):
        return [col for col in range(self.COLUMNS) if self.is_valid_location(col)]

    def drop_piece(self, col, token):
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY_SLOT:
                self.board[row][col] = token
                return

    def make_move(self, col):
        self.drop_piece(col, self.current_player)
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def winning_move(self, token):
        # Check horizontal locations
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == token and \
                   self.board[row][col+1] == token and \
                   self.board[row][col+2] == token and \
                   self.board[row][col+3] == token:
                    return True

        # Check vertical locations
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                if self.board[row][col] == token and \
                   self.board[row+1][col] == token and \
                   self.board[row+2][col] == token and \
                   self.board[row+3][col] == token:
                    return True

        # Check positively sloped diagonals
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == token and \
                   self.board[row+1][col+1] == token and \
                   self.board[row+2][col+2] == token and \
                   self.board[row+3][col+3] == token:
                    return True

        # Check negatively sloped diagonals
        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == token and \
                   self.board[row-1][col+1] == token and \
                   self.board[row-2][col+2] == token and \
                   self.board[row-3][col+3] == token:
                    return True

        return False

    def is_board_full(self):
        for col in range(self.COLUMNS):
            if self.is_valid_location(col):
                return False
        return True

    def is_game_over(self):
        return self.winning_move('X') or self.winning_move('O') or self.is_board_full()

    def clone(self):
        new_state = GameState()
        new_state.board = [row[:] for row in self.board]
        new_state.current_player = self.current_player
        return new_state
