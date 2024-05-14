from game_state import GameState
from QLearning import QLearningBot

def train_q_learning_bot(episodes=1000):
    bot = QLearningBot(token='X')
    opponent = QLearningBot(token='O')
    
    for episode in range(episodes):
        state = GameState()
        while not state.is_game_over():
            current_bot = bot if state.current_player == 'X' else opponent
            action = current_bot.choose_action(state)
            state.make_move(action)
            reward = 1 if state.winning_move(current_bot.token) else 0
            next_state = state.clone()
            bot.update_q_value(state, action, reward, next_state)
            state = next_state
            if state.is_game_over():
                break
        if episode % 500 == 0:
            print(f"Episode {episode + 1}/{episodes} completed.")

    bot.save_q_table('q_table.pkl')
    return bot

if __name__ == "__main__":
    trained_bot = train_q_learning_bot(episodes=100000)
    print("Training completed.")
