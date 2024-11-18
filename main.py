from agent import RandomAgent
from blackjack import Blackjack

bj = Blackjack()

print(bj.play_round(RandomAgent()))

print(bj.wins, bj.losses, bj.ties)