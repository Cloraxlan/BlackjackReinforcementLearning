from agent import QLearningAgent
from blackjack import Blackjack
from main import play_round_demo

bj = Blackjack()


qla = QLearningAgent(0.1, 0.1, 0.6, False)
qla.train(bj.initial_state, bj, 10000)
play_round_demo(bj, qla)
