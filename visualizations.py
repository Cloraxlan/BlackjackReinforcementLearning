from matplotlib import pyplot as plt
import numpy as np
from agent import Agent
from blackjack import Blackjack
import pandas as pd

def round_compare_visualization(bj : Blackjack, states, actions, compare_agent : Agent, main_agent_name, compare_agent_name):
    """
    Method used to compare the action taken by each agent against another over 1 shuffle round
    :param bj: The problem (Blackjack) agent
    :param states: States given to each agent
    :param actions: Actions taken by the main agent
    :param compare_agent: Agent compared to the main agent
    :param main_agent_name: The main agent
    :param compare_agent_name: Name of the comparison agent
    """
    df = pd.DataFrame(columns=["Player Cards", "Known Dealer Cards", f"{main_agent_name} Action", f"{compare_agent_name} Action"])
    alternative_actions = []
    for i, state in enumerate(states):
        alternative_actions.append(compare_agent.get_action(state, bj))
        df.loc[len(df)] = [state[1], state[2], actions[i],alternative_actions[i] ]
    df['']
    df.to_html(f"./{main_agent_name}_compared_to_{compare_agent_name}.html")


def plot_wins(agents_names_arr , results_arr):
    """
    Method used to plot the number of wins in a line graph
    :param agents_names_arr: Names of the agents used
    :param results_arr: List that contains the results
    """
    for results in results_arr:
        y_hist = [0]
        y = 0
        X = np.arange(0,len(results)+1,1)
        for result in results:
            if result == Blackjack.GameState.WIN:
                y += 1
            y_hist.append(y)
        plt.plot(X,y_hist)
    plt.title(f"Total wins Comparison")
    plt.xlabel("Games Played")
    plt.ylabel("Total wins")
    plt.legend(agents_names_arr)
    plt.savefig(f'wins.png') 

def bar_plot_wins(num_shuffle, agents_names_arr , results_arr):
    """
    Method used to plot the bar graph to compare number of wins per agent
    :param num_shuffle: Number of shuffles
    :param agents_names_arr: Names of the agents used
    :param results_arr: List that contains the results
    """
    plt.figure(figsize=(15, 5))
    for name, result in zip(agents_names_arr, results_arr):
        wins = result.count(Blackjack.GameState.WIN)
        plt.bar(f"{name}\n{wins} total wins", wins)
    plt.title(f"Total wins with {num_shuffle} shuffles")
    plt.ylabel("Total wins")
    plt.savefig(f'wins.png') 

def epoch_bar_comparison(num_shuffle, epochs, results_arr):
    """
    Method used to plot the bar graph to compare performances of various epoch counts.
    :param num_shuffle: Number of shuffles
    :param epochs: Number of epochs
    :param results_arr: List that contains the results
    """
    plt.figure(figsize=(15, 5))
    for epoch_count, result in zip(epochs, results_arr):
        wins = result.count(Blackjack.GameState.WIN)
        plt.bar(f"{epoch_count} Epochs\n{wins} total wins", wins)
    plt.title(f"Total wins with {num_shuffle} shuffles")
    plt.ylabel("Total wins")
    plt.savefig(f'wins_epochs.png') 