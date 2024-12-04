    
from local_search import GeneticAlgorithm
from local_search_problem import Hyperparams


if __name__ == "__main__":
    search = GeneticAlgorithm(50, 10)
    search.run(Hyperparams(10000, False))