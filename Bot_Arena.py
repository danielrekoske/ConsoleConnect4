from game_state import GameState, EMPTY_SLOT
from bot_player import BotPlayer

class BotBattle:
    def __init__(self, bot1, bot2):
        self.bot1 = bot1
        self.bot2 = bot2
        self.results = {'bot1_wins': 0, 'bot2_wins': 0, 'draws': 0}

    def play_game(self):
        game_state = GameState()
        bots = { 'X': self.bot1, 'O': self.bot2 }
        while not game_state.is_game_over():
            current_bot = bots[game_state.current_player]
            move = current_bot.get_move(game_state)
            game_state.make_move(move)
        
        if game_state.winning_move('X'):
            self.results['bot1_wins'] += 1
        elif game_state.winning_move('O'):
            self.results['bot2_wins'] += 1
        else:
            self.results['draws'] += 1

    def play_multiple_games(self, num_games):
        for _ in range(num_games):
            self.play_game()
        return self.results
