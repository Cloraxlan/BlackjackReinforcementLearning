from agent import RandomAgent, CardCountingAgent, BasicStrategyAgent
from blackjack import Blackjack
from visualizations import plot_wins, round_compare_visualization

bj = Blackjack()

def play_round(bj, agent):
        actions = []
        states = []
        bj.shuffle()
        wins = 0
        losses = 0
        ties = 0
        results = []
        while True:
            curr_game_actions = []
            curr_game_states = []
            result = bj.start_game()
            if result is bj.GameState.OUT_OF_CARDS:
                    return states, actions, (wins, losses, ties), results
            game_over = False
            curr_game_states.append(bj.get_state())
            curr_game_actions.append(agent.get_action(bj.get_state(), bj))
            while curr_game_actions[-1]  == bj.Action.HIT:
                result = bj.hit()
                if result is bj.GameState.LOSS:
                    losses += 1
                    game_over = True
                    actions += curr_game_actions
                    states += curr_game_states
                    results.append(result)
                    break
                if result is bj.GameState.OUT_OF_CARDS:
                    return states, actions, (wins, losses, ties), results
                curr_game_actions.append(agent.get_action(bj.get_state(), bj))
                curr_game_states.append(bj.get_state())
            if game_over:
                continue
            result = bj.stand()
            if result is bj.GameState.OUT_OF_CARDS:
                return states, actions, (wins, losses, ties), results
            if result is bj.GameState.LOSS:
                losses += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)
            if result is bj.GameState.WIN:
                wins += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)
            if result is bj.GameState.TIE:
                ties += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)

def play_multiple_rounds(n, agent):
    all_result = []
    for i in range(n):
        _, _, _, results = play_round(bj, agent)
        all_result += results
    return all_result



#states, actions, _, results = play_round(bj, CardCountingAgent())
#round_compare_visualization(bj, states, actions, RandomAgent())
plot_wins(("Random Agent", "Basic Strategy", "Card counting Agent"), (play_multiple_rounds(50, RandomAgent()), play_multiple_rounds(50, BasicStrategyAgent()),play_multiple_rounds(50, CardCountingAgent())))
#round_compare_visualization(bj, states, actions, RandomAgent(), "Card Counting Agent", "Random Agent")