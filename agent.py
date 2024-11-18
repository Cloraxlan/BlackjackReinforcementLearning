from abc import ABC, abstractmethod
import random

class Agent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, curr_state, actions):
        pass

class RandomAgent(Agent):

    def get_action(self, curr_state, actions):
        return random.choice(actions)
