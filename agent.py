from abc import ABC, abstractmethod
import random
import math
from blackjack import Blackjack
import pickle

class Agent(ABC):
    """
    Base agent for a blackjack player.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, curr_state,  problem: Blackjack):
        """
        Return an action given the current state and the problem.

        :param curr_state: List containing a list of all the played cards,
         list of the player's hand and a list of the dealer's hand.
        :param problem: Class that represents the problem with various operators.
        :return: Action to perform in this state.
        """
        pass

    def random_action(self, problem : Blackjack):
        """
        Returns a random action given the current state and the problem.
        :param problem: Class that represents the problem with various operators.
        :return: Random action to perform in this state.
        """
        return random.choice(problem.actions)

class RandomAgent(Agent):
    """
    Blackjack player agent that randomly chooses an action for a given state.
    """
    def get_action(self, curr_state, problem: Blackjack):
        """
        Return an action given the current state and the problem.

        :param curr_state: List containing a list of all the played cards,
        list of the player's hand and a list of the dealer's hand.
        :param problem: Class that represents the problem with various operators.
        :return: A random action to perform in this state.
        """
        return random.choice(problem.actions)

class CardCountingAgent(Agent):
    """
    Blackjack player agent that uses card counting techniques to make an informed decision.
    """

    "Variable to keep track of the running count"
    running_count = 0

    "Variable to indicate a HIT as an integer"
    HIT = 100

    "Variable to indicate a STAND as an integer"
    STAND = -100

    """2d array of actions to perform, player and dealer hand values are used for
     indices to get the action. Makes use of the true count for decision if an
    action found isn't a HIT/STAND"""
    illustrious_18_chart = [[HIT, HIT, HIT, HIT, HIT, HIT, HIT, 1, HIT, HIT, 3, -1, STAND,
                             STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 2, -2, STAND,
                             STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 0, 0, STAND,
                             STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -2, STAND,
                             STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, -1, STAND,
                             STAND, STAND, STAND, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, 3, HIT, HIT, HIT, HIT, HIT,
                             HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT,
                             HIT, HIT, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT,
                             HIT, 5, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 4, HIT, HIT, HIT, HIT,
                             4, 0, STAND, STAND, STAND, STAND, STAND],
                            [HIT, HIT, HIT, HIT, HIT, HIT, HIT, HIT, 4, 1, HIT, HIT, HIT, HIT,
                             HIT, STAND, STAND, STAND, STAND, STAND]]

    def __init__(self):
        super().__init__()


    def get_action(self, curr_state, problem: Blackjack):
        """
        Return an action given the current state and the problem.
        :param curr_state: List containing a list of all the played cards,
        list of the player's hand and a list of the dealer's hand.
        :param problem: Class that represents the problem with various operators.
        :return: An action to perform in this state based on the player and dealer hand values.
        """
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

class QLearningAgent(Agent):
    """
    QLearning agent that uses the player hand and dealer's hand (if specified)
     as the state to find the action
    """
    def __init__(self, epsilon: float, alpha: float, gamma: float, use_dealer_hand):
        super().__init__()
        self._table = {}
        self._actions_per_state = 2
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma
        self.use_dealer_hand = use_dealer_hand

    def table(self):
        """
        Returns the q-table
        :return: Trained q-table
        """
        return self._table
    
    def get_state_key(self, state, problem):
        """
        Method used to get the state key for the needed q-table
        :param state: List containing a list of all the played cards,
        list of the player's hand and a list of the dealer's hand
        :param problem: Class that represents the problem with various operators.
        :return: State to use as the key for the q-table
        """
        if self.use_dealer_hand:
            return (problem.val(state[1]),problem.val(state[2]))
        else:
            return problem.val(state[1])

    def get_action(self, current_state, problem: Blackjack):
        """
        Return an action given the current state and the problem.
        :param current_state: List containing a list of all the played cards,
        list of the player's hand and a list of the dealer's hand
        :param problem: Class that represents the problem with various operators.
        :return: An Action based off the state and the q-table.
        """
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
        """
        Method used to train the QLearning agent's table
        :param inital_state: Initial state of problem
        :param problem: Class that represents the problem with various operators.
        :param num_epochs: Number of epochs to train the agent
        :param num_iterations: Number of iterations per epoch to train the agent
        """
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

    def export_table(self, file_name):
        """
        Method used to export table as a pkl file to be used for later
        :param file_name: File name to store the q-table in.
        """
        with open(file_name, 'wb') as f:
            pickle.dump(self.table(), f)
            
    def load_table(self, file_name):
        """
        Method used to load the q-table from a pkl file.
        :param file_name: File name of the stored q-table.
        """
        with open(file_name, 'rb') as f:
            self.table = pickle.load(f)

    def print_table(self, file_name):
        """
        Method used to print the q-table.
        :param file_name: Name of the pkl file that has the q-table.
        """
        with open(file_name, 'rb') as f:
            data_loaded = sorted(pickle.load(f))
        min_player = data_loaded[0][0]
        max_player = data_loaded[-1][0]
        print("   " + str(list(range(data_loaded[0][1], 22))))
        for i in range(min_player, max_player + 1):
            string_o = str(i) + "  "
            if i < 10:
                string_o += " "
            for item in data_loaded:
                if item[0] == i:
                    if self._table[item][0] > self._table[item][1]:
                        string_o += "H  "
                    else:
                        string_o += "S  "
                    if item[1] > 9:
                        string_o += " "
            print(string_o)