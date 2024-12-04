from abc import ABC, abstractmethod
import random
import math
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

class CardCountingAgent(Agent):
    running_count = 0
    HIT = 100
    STAND = -100
    illustrious_18_chart = [[HIT, HIT, HIT, HIT, HIT, HIT, HIT, 1, HIT, HIT, 3, -1, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 2, -2, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 0, 0, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -2, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -1, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, 3, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 5, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 4, HIT, HIT, HIT, HIT, 4, 0, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 4, 1, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND]]

    def __init__(self):
        super().__init__()

    def get_action(self, curr_state, problem: Blackjack):
        self.running_count = 0
        for item in curr_state[0]:
            if 1 <= item <= 6:
                self.running_count += 1
            elif item == 10:
                self.running_count -= 1
        decks = math.ceil(len(problem.deck) / 13)
        if len(curr_state[0]) == 208:
            decks = 1
        true_count = math.floor(self.running_count / decks)
        player_value = problem.val(curr_state[1])
        dealer_value = problem.val(curr_state[2])
        if player_value > 21:
            return problem.Action.STAND
        if self.illustrious_18_chart[dealer_value - 2][player_value - 2] == self.HIT:
            return problem.Action.HIT
        elif self.illustrious_18_chart[dealer_value - 2][player_value - 2] == self.STAND:
            return problem.Action.STAND
        else:
            to_check = self.illustrious_18_chart[dealer_value - 2][player_value - 2]
            if true_count < to_check:
                return problem.Action.HIT
            else:
                return problem.Action.STAND


class BasicStrategyAgent(Agent):
    HIT = 100
    STAND = -100
    basic_strategy = [[HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                      [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, STAND, STAND, STAND, STAND, STAND]]

    def __init__(self):
        super().__init__()

    def get_action(self, curr_state, problem: Blackjack):
        player_value = problem.val(curr_state[1])
        dealer_value = problem.val(curr_state[2])
        if player_value > 21:
            return problem.Action.STAND
        if self.basic_strategy[dealer_value - 2][player_value - 2] == self.HIT:
            return problem.Action.HIT
        else:
            return problem.Action.STAND

class QLearningAgent(Agent):
    def __init__(self, epsilon: float, alpha: float, gamma: float):
        super().__init__()
        self._table = {}
        self._actions_per_state = 2
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

    def table(self):
        return self._table

    def get_action(self, curr_state, problem: Blackjack):
        player_cards = tuple(curr_state[1])
        dealer_cards = tuple(curr_state[2])
        state_tuple = (player_cards, dealer_cards)
        if state_tuple not in self._table:
            self._table[state_tuple] = [0 for _ in range(2)]
        action = self._table[state_tuple].index(max(self._table[state_tuple]))

        if action == 0:
            return problem.Action.HIT
        else:
            return problem.Action.STAND

    def train(self, initial_state, problem: Blackjack, num_epochs: int = 100, num_iterations: int = 1000):
        player_cards = tuple(initial_state[1])
        dealer_cards = tuple(initial_state[2])
        state_tuple = (player_cards, dealer_cards)
        for i in range(num_epochs):
            current = state_tuple
            for j in range(num_iterations):
                value = random.random()
                action = None
                if value < self._epsilon:
                    action = random.choice(problem.actions)
                else:
                    action = self.get_action(current, problem)
                goal_state = None
                new_state = None
                if action == problem.Action.HIT:
                    new_state = problem.hit()
                    goal_state = problem.get_state()
                else:
                    new_state = problem.stand()
                    goal_state = problem.get_state()
                reward = None
                if new_state is problem.GameState.WIN:
                    reward = 10
                else:
                    reward = -1
                current_q = self._table[state_tuple][problem.actions.index(action)]
                max_action = self.get_action(new_state, problem)
                max_possible_q = self._table[(new_state[1], new_state[2])][problem.actions.index(action)]
                new_q = ((1 - self._alpha) * current_q) + self._alpha * (reward + (self._gamma * max_possible_q))
                self._table[state_tuple][problem.actions.index(action)] = new_q
                current = new_state
                if problem.GameState.WIN:
                    break