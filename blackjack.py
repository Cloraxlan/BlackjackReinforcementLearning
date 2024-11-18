from enum import Enum
import random
from agent import Agent

class Blackjack:

    class GameState(Enum):
        IN_PROGRESS = 1
        WIN = 2
        LOSS = 3
        TIE = 4
        OUT_OF_CARDS = 5
    
    class Action(Enum):
        HIT = 1
        STAND = 2

    def __init__(self, num_decks=4, dealer_value_limit=17):
        self.num_decks = num_decks
        self.dealer_value_limit = dealer_value_limit
        self.deck = []
        self.played_cards = []
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.actions = [self.Action.HIT, self.Action.STAND]

    def shuffle(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.deck.clear()
        self.played_cards.clear()
        for _ in range(self.num_decks):
            self.deck += range(1,10)
            self.deck += (10,10,10)
        random.shuffle(self.deck)

    def next_card(self):
        new_card = self.deck.pop()
        self.played_cards.append(new_card)
        return new_card
    
    def has_next_card(self):
        return len(self.deck) > 0
    
    def get_state(self):
         return [self.played_cards, self.player_cards, self.dealer_cards]
        
    def val(self, deck):
        deck_val = sum(deck)
        if 1 in deck:
            if deck_val + 9 <= 21:
                deck_val += 9
        return deck_val

    def start_game(self):        
        self.player_cards = []
        self.dealer_cards = []

        if len(self.deck) < 3:
             return self.GameState.OUT_OF_CARDS

        self.player_cards.append(self.next_card())
        self.player_cards.append(self.next_card())

        self.dealer_cards.append(self.next_card())

        return self.GameState.IN_PROGRESS
    
    def hit(self):
        if not self.has_next_card():
            return self.GameState.OUT_OF_CARDS
        new_card = self.next_card()
        self.player_cards.append(new_card)

        if self.val(self.player_cards) > 21:
            return self.GameState.LOSS
        
        return self.GameState.IN_PROGRESS
    
    def stand(self):
        new_cards = []
        while self.val(self.dealer_cards) < self.dealer_value_limit and self.val(self.dealer_cards) < 21:
            if not self.has_next_card():
                return self.GameState.OUT_OF_CARDS
            new_card = self.next_card()
            self.dealer_cards.append(new_card)
            new_cards.append(new_card)
        
        if self.val(self.dealer_cards) > 21:
            return self.GameState.WIN
        
        if self.val(self.dealer_cards) < self.val(self.player_cards):
            return self.GameState.WIN
        elif self.val(self.dealer_cards) > self.val(self.player_cards):
            return self.GameState.LOSS
        else:
            return self.GameState.WIN

    def play_round(self, agent: Agent):
        actions = []
        self.shuffle()
        
        while True:
            curr_game_actions = []
            result = self.start_game()
            if result is self.GameState.OUT_OF_CARDS:
                    return actions
            game_over = False
            curr_game_actions.append(agent.get_action(self.get_state(), self.actions))
            while curr_game_actions[-1]  == self.Action.HIT:
                result = self.hit()
                if result is self.GameState.LOSS:
                    self.losses += 1
                    self.game_over = True
                    actions += curr_game_actions
                if result is self.GameState.OUT_OF_CARDS:
                    return actions
                curr_game_actions.append(agent.get_action(self.get_state(), self.actions))
            if game_over:
                continue
            result = self.stand()
            if result is self.GameState.OUT_OF_CARDS:
                    return actions
            if result is self.GameState.LOSS:
                    self.losses += 1
                    actions += curr_game_actions
            if result is self.GameState.WIN:
                    self.wins += 1
                    actions += curr_game_actions
            if result is self.GameState.TIE:
                    self.ties += 1
                    actions += curr_game_actions


                    

