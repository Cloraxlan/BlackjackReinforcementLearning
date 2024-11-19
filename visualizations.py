from matplotlib import pyplot as plt
import numpy as np
from agent import Agent
from blackjack import Blackjack
import pandas as pd

def round_compare_visualization(bj : Blackjack, states, actions, compare_agent : Agent):
    df = pd.DataFrame(columns=["Player Cards", "Known Dealer Cards", "Agent 1 Action", "Agent 2 Action"])
    alternative_actions = []
    for i, state in enumerate(states):
        alternative_actions.append(compare_agent.get_action(state, bj))
        df.loc[len(df)] = [state[1], state[2], actions[i],alternative_actions[i] ]
    df.to_html("./test.html")


def plot_wins(results, agent_name):
    y_hist = [0]
    y = 0
    X = np.arange(0,len(results)+1,1)
    for result in results:
        if result == Blackjack.GameState.WIN:
            y += 1
        y_hist.append(y)

    plt.plot(X,y_hist)
    plt.title(f"Total wins using {agent_name}")
    plt.xlabel("Games Played")
    plt.ylabel("Total wins")
    plt.savefig(f'wins_{agent_name}.png') 

