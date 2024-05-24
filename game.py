from game_state import GameState
from Player import HumanPlayer
from bot_player import BotPlayer

class Game:
    PLAYER1_TOKEN = 'X'
    PLAYER2_TOKEN = 'O'

    def __init__(self, bot_difficulty):
        self.game_state = GameState()
        self.players = [
            HumanPlayer(self.PLAYER1_TOKEN),
            BotPlayer(self.PLAYER2_TOKEN, bot_difficulty)
        ]
        self.turn = 0

    def play(self):
        self.game_state.print_board()

        while True:
            current_player = self.players[self.turn % 2]
            move = current_player.get_move(self.game_state)
            self.game_state.drop_piece(move, current_player.token)

            self.game_state.print_board()

            if self.game_state.winning_move(current_player.token):
                print(f"Congratulations! Player {current_player.token} wins!")
                break
            elif self.game_state.is_board_full():
                print("It's a tie!")
                break

            self.turn += 1

if __name__ == "__main__":
    bot_difficulty = int(input("Choose bot difficulty level (0-5): "))
    if bot_difficulty < 0 or bot_difficulty > 5:
        print("Invalid difficulty level! Please choose a level between 0 and 5.")
    else:
        game = Game(bot_difficulty)
        game.play()
