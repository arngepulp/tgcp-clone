import sys
import os
import json
import random
from engine.models.card import load_card
# from engine.rules.game_rules import PTS_TO_WIN

def load_deck(path):
    with open(path) as file:
        data = json.load(file)
        
        deck = []
        for card in data["cards"]:
            for _ in range(card["count"]):
                deck.append(card["id"])
        return deck
    
def draw_opening_hand(self):
    
    
    # find first basic pokemon
    for i, card_id in enumerate(self.deck):
        card = load_card(card_id)
        if card.evolves_from is None:
            self.hand.append(card_id)
            self.deck.pop(i)
            break
    
    # draw remaining 4
    for _ in range(4):
        self.draw_card()
    
    
class Player:
    def __init__(self,deck_name):
        self.pts = 0
        
        #board
        self.deck_name = deck_name
        self.active = None
        self.bench = [None, None, None]
        self.path = f"decks/{deck_name}.json"
        self.deck = load_deck(self.path)
        random.shuffle(self.deck)
        self.hand = [] ## TODO once implementing longer decks cards should be drawn automatically for first turn.
        self.discard = []
        
        self.attached_energy = False
        self.has_attacked = False
    
    def __repr__(self):
        return f"{self.deck_name} | PTS: {self.pts} | Active: {self.active} | Bench: {self.bench}"
        
        
        
    def add_pts(self, n):
        self.pts += n
        '''
        if self.pts >= PTS_TO_WIN:
            # TODO win game
            pass
            '''
        
    def draw_card(self):
        new_card = self.deck.pop(0)
        self.hand.append(new_card)
        