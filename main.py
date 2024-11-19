from agent import RandomAgent
from blackjack import Blackjack
from visualizations import round_compare_visualization

bj = Blackjack()

def play_round(bj, agent):
        actions = []
        states = []
        end_indexes = []
        bj.shuffle()     
        wins = 0
        losses = 0
        ties = 0
        while True:
            curr_game_actions = []
            curr_game_states = []
            result = bj.start_game()
            if result is bj.GameState.OUT_OF_CARDS:
                    return states, actions, (wins, losses, ties), end_indexes
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
                    end_indexes.append(len(states)-1)
                    break
                if result is bj.GameState.OUT_OF_CARDS:
                    return states, actions, (wins, losses, ties), end_indexes
                curr_game_actions.append(agent.get_action(bj.get_state(), bj))
                curr_game_states.append(bj.get_state())
            if game_over:
                continue
            result = bj.stand()
            if result is bj.GameState.OUT_OF_CARDS:
                    return states, actions, (wins, losses, ties), end_indexes
            if result is bj.GameState.LOSS:
                    losses += 1
                    actions += curr_game_actions
                    states += curr_game_states
                    end_indexes.append(len(states)-1)
            if result is bj.GameState.WIN:
                    wins += 1
                    actions += curr_game_actions
                    states += curr_game_states
                    end_indexes.append(len(states)-1)
            if result is bj.GameState.TIE:
                    ties += 1
                    actions += curr_game_actions
                    states += curr_game_states
                    end_indexes.append(len(states)-1)

states, actions, _, end_indexes= play_round(bj, RandomAgent())
round_compare_visualization(bj, states, actions, end_indexes, RandomAgent())                    



print()
