from time import sleep
from agent import QLearningAgent, RandomAgent, CardCountingAgent, BasicStrategyAgent
from blackjack import Blackjack
from visualizations import bar_plot_wins, epoch_bar_comparison, plot_wins, round_compare_visualization

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

def play_round_demo(bj, agent):
        actions = []
        states = []
        bj.shuffle()
        wins = 0
        losses = 0
        ties = 0
        results = []
        while True:
            print("\n\n")
            sleep(3)
            curr_game_actions = []
            curr_game_states = []
            result = bj.start_game()
            if result is bj.GameState.OUT_OF_CARDS:
                    print("out of cards")
                    return states, actions, (wins, losses, ties), results
            print(f"Player Hand  {bj.get_state()[1]}")
            print(f"Dealer Hand  {bj.get_state()[2]}")
            game_over = False
            curr_game_states.append(bj.get_state())
            curr_game_actions.append(agent.get_action(bj.get_state(), bj))
            while curr_game_actions[-1]  == bj.Action.HIT:
                print("hit")
                result = bj.hit()
                print(f"Player Hand  {bj.get_state()[1]}")
                print(f"Dealer Hand  {bj.get_state()[2]}")
                if result is bj.GameState.LOSS:
                    print("loss")
                    losses += 1
                    game_over = True
                    actions += curr_game_actions
                    states += curr_game_states
                    results.append(result)
                    break
                if result is bj.GameState.OUT_OF_CARDS:
                    print("out of cards")
                    return states, actions, (wins, losses, ties), results
                curr_game_actions.append(agent.get_action(bj.get_state(), bj))
                curr_game_states.append(bj.get_state())
            if game_over:
                continue
            print("stand")
            result = bj.stand()
            print(f"Player Hand  {bj.get_state()[1]}")
            print(f"Dealer Hand  {bj.get_state()[2]}")
            if result is bj.GameState.OUT_OF_CARDS:
                print("out of cards")
                return states, actions, (wins, losses, ties), results
            if result is bj.GameState.LOSS:
                print("loss")
                losses += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)
            if result is bj.GameState.WIN:
                print("win")
                wins += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)
            if result is bj.GameState.TIE:
                print("tie")
                ties += 1
                actions += curr_game_actions
                states += curr_game_states
                results.append(result)


if __name__ == "__main__":
    #qla = QLearningAgent(0.1, 0.1, 0.6, False)
    #qla.train(bj.initial_state, bj, 10000)
    #qla2 = QLearningAgent(0.4, 0.4, 0.5, True)
    #qla2.train(bj.initial_state, bj, 10000)
    #states, actions, _, results = play_round(bj, CardCountingAgent())
    #round_compare_visualization(bj, states, actions, qla, "Card Counting Agent", "QLearn Player Hand Agent")
    #round_compare_visualization(bj, states, actions, qla2, "Card Counting Agent", "QLearn All Hand Agent")
    qla = QLearningAgent(0.4, 0.4, 0.5, False)
    qla.train(bj.initial_state, bj, 100000)
    qla2 = QLearningAgent(0.4, 0.4, 0.5, True)
    qla2.train(bj.initial_state, bj, 100000)
    states, actions, _, results = play_round(bj, CardCountingAgent())
    round_compare_visualization(bj, states, actions, qla, "Card Counting Agent", "QLearn Player Hand Agent")
    round_compare_visualization(bj, states, actions, qla2, "Card Counting Agent", "QLearn All Hand Agent")


    qla2.export_table("test.pkl")
    qla2.print_table("test.pkl")
    
    #plot_wins(("QLearning Agent(Player Hand Only)", "QLearning Agent(All Known Cards)"), (play_multiple_rounds(50, qla), play_multiple_rounds(50, qla2)))
    bar_plot_wins(50, ("QLearning Agent(Player Hand Only)\n100000 Epochs", "QLearning Agent(All Known Cards)\n100000 Epochs", "Random Agent", "Card Counting Agent"), (play_multiple_rounds(50, qla), play_multiple_rounds(50, qla2), play_multiple_rounds(50, RandomAgent()),play_multiple_rounds(50, CardCountingAgent())))
    #epoch_bar_comparison(50, (10,100,1000,10000), (play_multiple_rounds(50, qla), play_multiple_rounds(50, qla2), play_multiple_rounds(50, qla3), play_multiple_rounds(50, qla4)))
    #round_compare_visualization(bj, states, actions, RandomAgent(), "Card Counting Agent", "Random Agent")