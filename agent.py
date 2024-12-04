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

    def random_action(self, problem : Blackjack):
        return random.choice(problem.actions)

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
    def __init__(self, epsilon: float, alpha: float, gamma: float, use_dealer_hand):
        super().__init__()
        self._table = {}
        self._actions_per_state = 2
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma
        self.use_dealer_hand = use_dealer_hand

    def table(self):
        return self._table
    
    def get_state_key(self, state, problem):
        if self.use_dealer_hand:
            return (problem.val(state[1]),problem.val(state[2]))
        else:
            return problem.val(state[1])

    def get_action(self, current_state, problem: Blackjack):
        if (self.get_state_key(current_state, problem)) not in self._table:
            self._table[self.get_state_key(current_state, problem)] = [0 for _ in range(self._actions_per_state)]
        actions = problem.actions
        max_q_val = float("-inf")
        max_action_index = -1
        for action in actions:
            if action is None:
                continue
            action_index = problem.actions.index(action)
            q_val = self._table[self.get_state_key(current_state, problem)][action_index]
            if q_val > max_q_val:
                max_q_val = q_val
                max_action_index = action_index
            elif q_val == max_q_val:
                if random.random() < 0.5:
                    max_q_val = q_val
                    max_action_index = action_index
        return problem.actions[max_action_index]

    def train(self, inital_state, problem: Blackjack, num_epochs: int = 100, num_iterations: int = 1000):
        for i in range(num_epochs):
            current_state = inital_state()
            done = False
            for j in range(num_iterations):
                if done:
                    break
                
                if random.random() <= self._epsilon:
                    action = self.random_action(problem)
                else:
                    action = self.get_action(current_state, problem)

                new_state = problem.result(current_state, action)

                reward = problem.reward(current_state, action)
                
                if problem.is_terminal(new_state, action):
                    done = True
                if (self.get_state_key(current_state, problem)) not in self._table:
                    self._table[self.get_state_key(current_state, problem)] = [0 for _ in range(self._actions_per_state)]
                curr_q = self._table[self.get_state_key(current_state, problem)][problem.actions.index(action)]
                if (self.get_state_key(new_state, problem)) not in self._table:
                    self._table[self.get_state_key(new_state, problem)] = [0 for _ in range(self._actions_per_state)]
                max_q = max(self._table[self.get_state_key(new_state, problem)])
                
                new_q = (1-self._alpha)*curr_q+self._alpha*(reward + self._gamma * max_q)
                
                self._table[self.get_state_key(current_state, problem)][problem.actions.index(action)] = new_q
                current_state = new_state
