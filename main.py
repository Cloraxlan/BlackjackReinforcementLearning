from agent import RandomAgent
from blackjack import Blackjack

bj = Blackjack()

def play_round(bj, agent):
        actions = []
        bj.shuffle()     
        wins = 0
        losses = 0
        ties = 0
        while True:
            curr_game_actions = []
            result = bj.start_game()
            if result is bj.GameState.OUT_OF_CARDS:
                    return actions, (wins, losses, ties)
            game_over = False
            curr_game_actions.append(agent.get_action(bj.get_state(), bj))
            while curr_game_actions[-1]  == bj.Action.HIT:
                result = bj.hit()
                if result is bj.GameState.LOSS:
                    losses += 1
                    bj.game_over = True
                    actions += curr_game_actions
                if result is bj.GameState.OUT_OF_CARDS:
                    return actions, (wins, losses, ties)
                curr_game_actions.append(agent.get_action(bj.get_state(), bj))
            if game_over:
                continue
            result = bj.stand()
            if result is bj.GameState.OUT_OF_CARDS:
                    return actions, (wins, losses, ties)
            if result is bj.GameState.LOSS:
                    losses += 1
                    actions += curr_game_actions
            if result is bj.GameState.WIN:
                    wins += 1
                    actions += curr_game_actions
            if result is bj.GameState.TIE:
                    ties += 1
                    actions += curr_game_actions


                    



print(play_round(bj, RandomAgent()))
