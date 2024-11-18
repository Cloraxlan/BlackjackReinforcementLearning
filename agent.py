from abc import ABC, abstractmethod
import random

from blackjack import Blackjack

class Agent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, curr_state,  problem: Blackjack):
        pass

class RandomAgent(Agent):

    def get_action(self, curr_state, problem: Blackjack):
        return random.choice(problem.actions)
