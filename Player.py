from game_state import GameState
class Player:
    def __init__(self, token):
        self.token = token

    def get_move(self, game_state):
        pass

class HumanPlayer(Player):
    def get_move(self, game_state):
        while True:
            try:
                col = int(input(f"Player {self.token}, enter column (1-7): ")) - 1
                if col < 0 or col >= GameState.COLUMNS:
                    print("Invalid column! Column number should be between 1 and 7.")
                    continue
                if game_state.is_valid_location(col):
                    return col
                else:
                    print("Column is full!")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 7.")
