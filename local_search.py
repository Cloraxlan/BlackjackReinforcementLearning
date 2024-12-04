import random
from typing import List, Optional

import numpy as np

from local_search_problem import LSProblem


class GeneticAlgorithm():

    def __init__(self, pop_size:int, num_epochs:int = 100, mutation_rate:float = 0.1 ):
        super().__init__()
        self.mutation_rate = mutation_rate
        self.num_epochs = num_epochs
        self.pop_size = pop_size



    def run(self, problem: LSProblem) -> [List[float], Optional[List[float]]]: # type: ignore
        """
        Runs Genetic Algorithm search with elitism.

        :param problem: Object that contains operators for performing a Local Search
        such as getting the value of a state, generating the successors of a state,
        and creating a new random state.
        :return: Returns a pair where the first value is a list of floats
        that represents the best solution. The second value is either None
        or are the scores of the best solution for each epoch.
        """
        
        population = []
        top_vals = []
        for i in range(self.pop_size):
            population.append(problem.new_state())
        for i in range(1, self.num_epochs):
            weights = []
            for state in population:
                weights.append(problem.value(state,True))
            top_vals.append(weights[np.argmax(weights)])
            population2 = []
            top_ind = population[np.argmax(weights)]
            for i in range(self.pop_size):
                parent1, parent2 = problem.selection(population, weights, 2)
                child = problem.crossover(parent1, parent2)
                if random.random() <= self.mutation_rate:
                    child = problem.mutate(child)
                population2.append(child)
            population2.append(top_ind)
            print(population[np.argmax(weights)])
            print(np.max(weights))
            population = population2
        weights = []
        for state in population:
            weights.append(problem.value(state,True))
        return population[np.argmax(weights)], top_vals
