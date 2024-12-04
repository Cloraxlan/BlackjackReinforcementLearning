import random
from copy import copy
from typing import List, Callable, Optional
from abc import ABC, abstractmethod
import numpy as np

from agent import QLearningAgent
from blackjack import Blackjack
from main import play_multiple_rounds


class LSProblem(ABC):
    """
    Base abstract class for problems that can be used with a Local
    Search algorithms. Assumes a state is a list of floats. Contains
    methods that return the value of the state, neighbors of the state,
    and a new random state.
    """
    def __init__(self):
        pass

    @abstractmethod
    def value(self, curr_state: List[float], maximize: bool) -> float:
        """
        Returns the value of the current state.

        If maximize is true, then bigger values are better.
        If maximize is false, then smaller values are better.

        :param curr_state: Current state to get a value for.
        :param maximize: Whether to adjust the output for maximization or minimization.
        :return: Value of the current state.
        """
        pass

    @abstractmethod
    def successors(self, current_state: List[float]) -> List[List[float]]:
        """
        Generates the successor of the current state.
        :param current_state: Current state (solution).
        :return: List of neighboring states.
        """
        pass

    @abstractmethod
    def new_state(self, seed: Optional[int] = None) -> List[float]:
        """
        Returns a new random state.

        :param seed: Random seed that will be set before generating the
        new state. If this is None, the random seed will not be set.
        :return: New random state.
        """
        pass

    def crossover(self, parent1: List[float], parent2: List[float]) -> List[float]:
        """
        Performs crossover on the passed in parents and returns a child.

        Performs single point crossover by generating a random crossover point c, and
        then returning the result of calling single_point_crossover(parent1, parent2, c)

        If crossover is not implemented in a problem, return the first parent.
        :param parent1: Parent state(genome) for crossover.
        :param parent2: Parent state(genome) for crossover.
        :return: Crossover combination of parent1 and parent2 if crossover
        is enabled, else just returns parent1.
        """
        c = random.randint(0, len(parent2)-1)
        return self.single_point_crossover(parent1, parent2, c)

    def single_point_crossover(self, parent1: List[float], parent2: List[float], c:int ) -> List[float]:
        """
        Performs single point crossover.

        If crossover is implemented, the resulting child's genome should be the
        beginning of parent1's genome up to and including c, plus parent2's genome
        from c to the end. If crossover is not implemented,
        :param parent1: Genome for parent 1.
        :param parent2: Genome for parent 2.
        :param c: The point in the genome to splice parent1 and parent 2 together.
        :return: Result of combing the beginning of parent1's genome up to and including c,
        plus parent2's genome from c to the end. If crossover is not implemented,
        returns a copy of parent1.
        """
        return parent1[0:c]+parent2[c:]
    
    def mutate(self, child: List[float]) -> List[float]:
        """
        Creates and returns a new state that is the affect of applying a mutation to child.

        If mutation is not enabled, returns a copy of the child.
        :param child: Child state to mutate. This passed in state is NOT modified.
        :return: Mutated copy of the child state or just a copy of the child state
        if mutation is not enabled
        """
        mutate_rate = 0.1
        child_copy = copy(child)
        for i in range(len(child_copy)):
            if random.random() < mutate_rate:
                self._mutate_bit(child_copy, i)
        return child_copy

    def _mutate_bit(self, child:List[float], index:int):
        """
        Mutates a single bit(gene) of the state(genome).

        For some problems mutating a bit could mean flipping a bit from 1 to 0,
        adding a random amount to the bit, swapping the bit with the adjacent bit, etc.
        :param child: Child state(genome) to mutate. This passed in state IS modified.
        :param index: Bit to mutate.
        """

        # _mutate_bit is implemented differently in each problem type so just pass here
        pass


    def selection(self, population: List[List[float]], weights: List[float], num_parents:int) -> List[List[float]]:
        """
        Performs selection on the passed in population and return n states as parents.

        This method performs fitness proportionate selection, also called roulette wheel selection.
        This method get the indices of the parents from the helper method _fitness_proportionate_selection.
        It then copies the states at those indices, puts them into a list, and returns that list.
        :param population: List of states(genomes) in the current population.
        :param weights: List of fitness values for each genome in current_population.
        Assumes bigger is better (maximization).
        :param num_parents: number of individuals to return from the selection
        :return: List of num_parents states
        """
        ret = []
        indices = self._fitness_proportionate_selection(weights, num_parents)
        for i in indices:
            ret.append(copy(population[i]))
        return ret

    def _fitness_proportionate_selection(self, weights: List[float], k:int) -> List[int]:
        """
        Performs fitness proportionate selection and returns indices for k selected individuals.

        Using the weights(fitness) values of each individual. Calculates the probability that
        each individual would be chosen randomly. It then chooses the indices for k individuals
        based on those probabilities. For example, if the passed-in weights where
        [3, 2, 5, 8, 2], then the resulting probabilities would be [0.15, 0.1, 0.25, 0.4, 0.1].
        We would then pick k indices of these based on those probabilities. Index 0 has a 0.15
        percent change to be chosen, index 1 has a 0.1 percent change to be chosen, index 2 has
        a 0.25 chance, etc.
        :param weights: List of fitness values for each genome in the population.
        Assumes bigger is better (maximization).
        :param k: Number of indices to return.
        :return: List of indices of individuals to choose.
        """
        choice = []
        for i in range(k):
            choice.append(self._fitness_proportionate_selection_single(weights, k))
        return choice
    def _fitness_proportionate_selection_single(self, weights: List[float], k:int) -> int:
        probs = []
        prob_sum = sum(weights)
        for weight in weights:
            if len(probs) > 0:
                probs.append(weight/prob_sum + probs[-1]) 
            else:
                probs.append(weight/prob_sum) 
        chance = random.random()
        for i, prob in enumerate(probs):
            if chance <= prob:
                return i


class Hyperparams(LSProblem):
    def __init__(self, num_epochs, use_dealer_deck):
        super().__init__()
        self.bj = Blackjack()
        self.num_epochs = num_epochs
        self.use_dealer_deck = use_dealer_deck
        

    def value(self, curr_state: List[float], maximize: bool) -> float:
        agent = QLearningAgent(curr_state[0], curr_state[1], curr_state[2], self.use_dealer_deck)
        agent.train(self.bj.initial_state, self.bj, self.num_epochs)
        return play_multiple_rounds(10, agent).count(self.bj.GameState.WIN)
        

    def successors(self, current_state: List[float]) -> List[List[float]]:
        scaling = 0.1
        s1 = copy(current_state)
        s1[0] += scaling * random.uniform(0, 1)
        succs = []
        for i in range(3):
            state1 = copy(current_state)
            state2 = copy(current_state)
            state1[i] += scaling * random.uniform(0, 1)
            state2[i] -= scaling * random.uniform(0, 1)
            succs.append(state1)
            succs.append(state2)
        return succs
    

    def new_state(self, seed: Optional[int] = None) -> List[float]:
        if seed is not None:
            random.seed(seed)
        return [random.random() for _ in range(3)]

    def _mutate_bit(self, child:List[float], index:int):
        child[index] += np.random.normal(0, 1)