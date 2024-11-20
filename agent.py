from abc import ABC, abstractmethod
import random
import math

from blackjack import Blackjack

class Agent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, curr_state, actions):
        pass

class RandomAgent(Agent):

    def get_action(self, curr_state, problem: Blackjack):
        return random.choice(problem.actions)

class CardCountingAgent(Agent):
    running_count = 0
    HIT = 100
    STAND = -100
    illustrious_18_chart = [[HIT, HIT, HIT, HIT, HIT, HIT, HIT, 1, HIT, HIT, 3, -1, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, 1, HIT, HIT, 3, -1, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, 1, HIT, HIT, 2, -2, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 0, 0, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -2, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -1, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, 3, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 5, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 4, HIT, HIT, HIT, HIT, 4, 0, STAND, STAND, STAND, STAND, STAND]]

    def __init__(self):
        super().__init__()

    def get_action(self, curr_state, problem: Blackjack):
        self.running_count = 0
        for item in curr_state[0]:
            if 1 <= item <= 6:
                self.running_count += 1
            elif item == 10:
                self.running_count -= 1
        decks = round(len(problem.deck) / 13) + 1
        true_count = math.floor(self.running_count / decks)
        player_value = problem.val(curr_state[1])
        dealer_value = problem.val(curr_state[2])
        if player_value > 21:
            return problem.Action.HIT
        if self.illustrious_18_chart[dealer_value - 1][player_value - 2] == self.HIT:
            return problem.Action.HIT
        elif self.illustrious_18_chart[dealer_value - 1][player_value - 2] == self.STAND:
            return problem.Action.STAND
        else:
            to_check = self.illustrious_18_chart[dealer_value - 1][player_value - 2]
            if true_count < to_check:
                return problem.Action.HIT
            else:
                return problem.Action.STAND


