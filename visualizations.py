from agent import Agent
from blackjack import Blackjack
import pandas as pd

def round_compare_visualization(bj : Blackjack, states, actions, end_indexes, compare_agent : Agent):
    df = pd.DataFrame(columns=["Player Cards", "Known Dealer Cards", "Agent 1 Action", "Agent 2 Action"])
    end_indexes.insert(0, 0)
    alternative_actions = []
    for i, state in enumerate(states):
        alternative_actions.append(compare_agent.get_action(state, bj))
        df.loc[len(df)] = [state[1], state[2], actions[i],alternative_actions[i] ]
    df.to_html("./test.html")



