"""
- Class: CSC 4631
- Section: 111
- Names: Konrad Rozpadek, Kalki Sarangan

File implementing methods to play 1 or more round(s) of blackjack, and play a demo round.
"""

from time import sleep
from agent import QLearningAgent, RandomAgent, CardCountingAgent, Agent
from blackjack import Blackjack
from visualizations import bar_plot_wins, epoch_bar_comparison, plot_wins, round_compare_visualization



def play_round(bj : Blackjack, agent: Agent) -> tuple[list[list[int]], list[Blackjack.Action], tuple[int], list[Blackjack.GameState]]:
    """
    Method used to play a round (play until a shuffle is needed).
    :param bj: The problem (blackjack) object
    :param agent: Type of agent to use for the game.
    """
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

def play_multiple_rounds(n : int, bj : Blackjack, agent : Agent) -> list[Blackjack.GameState]:
    """
    Method used to play multiple rounds of shuffles
    :param n: Number of shuffles
    :param agent: Agent to use for the game.
    :return: Results of all the hands
    """
    all_result = []
    for i in range(n):
        _, _, _, results = play_round(bj, agent)
        all_result += results
    return all_result

def play_round_demo(bj : Blackjack, agent : Agent) -> tuple[list[list[int]], list[Blackjack.Action], tuple[int], list[Blackjack.GameState]]:
    """
    Method used to play a demo round.
    :param bj: The problem (blackjack) object
    :param agent: Agent to use for the game.
    :return: Returns the states, actions taken, wins, losses, ties and results
    """
    actions = []
    states = []
    bj.shuffle()
    wins = 0
    losses = 0
    ties = 0
    results = []
    while True:
        print("\n\n")
        #sleep(3)
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
    """
    Runs demo with a agent
    """
    bj = Blackjack()
    agent_type = input("Select an Agent 1) Random\n 2) Card Counting\n 3) QLearning Player Hand State\n 4) QLearning All Hand State\n")
    agent_type = int(agent_type)
    if agent_type == 1:
        agent = RandomAgent()
    elif agent_type == 2:
        agent = CardCountingAgent()
    elif agent_type == 3:
        agent = QLearningAgent(0.1, 0.1, 0.6, False)
        agent.train(bj, 10000)
    elif agent_type == 4:
        agent = QLearningAgent(0.4, 0.4, 0.5, True)
        agent.train(bj, 10000)
    else:
        exit()
    
    play_round_demo(bj, agent)